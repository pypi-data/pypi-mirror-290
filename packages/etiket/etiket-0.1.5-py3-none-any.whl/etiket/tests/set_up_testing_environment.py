import os

database_file = "unit_testing.db"
# set up environmental variables
os.environ["DEBUSSY"] = "1"

os.environ["ETIKET_NAME"]="my_etiket"

os.environ["ETIKET_ADMIN_USERNAME"]="test_user"
os.environ["ETIKET_ADMIN_PASSWORD"]="qdrive#likes#testing"
os.environ["ETIKET_ADMIN_EMAIL"]="test@test.com"

os.environ["ETIKET_TOKEN_SECRET_KEY"]="c62c8072bb0fe4a63444058031ea354151af6ee44d95c8b550189c73b28e1114"

os.environ["POSTGRES_HOST"]="_"
os.environ["POSTGRES_USER"]="_"
os.environ["POSTGRES_PASSWORD"]="_"
os.environ["POSTGRES_DB"]="etiket_db"

os.environ["S3_ENDPOINT"]="http://0.0.0.0:4566"
os.environ["S3_BUCKET"]="test_bucket"
os.environ["S3_ACCESS_KEY_ID"]="test"
os.environ["S3_SECRET_ACCESS_KEY"]="test"

# remove any existing database.
if os.path.exists(database_file):
    os.remove(database_file)