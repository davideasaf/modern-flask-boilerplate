def add_users(db):
    db.session.add(
        User(username="admin", password=guard.hash_password("password"), roles="admin")
    )
    db.session.add(User(username="user", password=guard.hash_password("pass")))


def add_iris_dataset(db):
    from sklearn.datasets import load_iris
    import numpy as np
    import pandas as pd

    iris = load_iris()
    iris_df = pd.DataFrame(
        data=np.c_[iris["data"], iris["target"]],
        columns=["sep_length", "sep_width", "pet_length", "pet_width", "target"],
    )
    print(iris_df.head())
    print(iris_df.shape)

    db.session.bulk_insert_mappings(Iris, iris_df.to_dict(orient="records"))
