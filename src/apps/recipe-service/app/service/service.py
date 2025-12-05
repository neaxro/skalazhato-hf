from app.repository.postgres import PostgresRepository


class RecipeService():
    def __init__(self):
        self.repository = PostgresRepository()
    
    def test(self):
        return self.repository.test()
