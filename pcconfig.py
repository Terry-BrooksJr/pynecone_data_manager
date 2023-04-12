import pynecone as pc

config = pc.Config(
    app_name="pynecone_data_manager",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)
