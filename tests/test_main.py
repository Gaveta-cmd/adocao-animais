import pytest
from src.models import SessionLocal, Animal, engine, Base
from src.app import app


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with app.test_client() as client:
        yield client
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_cadastrar_animal(client, db):
    response = client.post("/cadastrar", data={
        "nome": "Rex",
        "especie": "Cachorro",
        "idade": "5",
        "raca": "Labrador",
        "observacoes": "Animal dócil"
    })
    assert response.status_code == 302
    animal = db.query(Animal).filter(Animal.nome == "Rex").first()
    assert animal is not None
    assert animal.especie == "Cachorro"


def test_listar_animais(client, db):
    novo = Animal(
        nome="Fluffy",
        especie="Gato",
        status="Disponível"
    )
    db.add(novo)
    db.commit()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Fluffy" in response.data


def test_adotar_animal(client, db):
    novo = Animal(
        nome="Bilu",
        especie="Cachorro",
        status="Disponível"
    )
    db.add(novo)
    db.commit()
    animal_id = novo.id
    response = client.post(f"/adotar/{animal_id}")
    assert response.status_code == 302
    animal_atualizado = db.query(Animal).filter(Animal.id == animal_id).first()
    assert animal_atualizado.status == "Adotado"


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}
