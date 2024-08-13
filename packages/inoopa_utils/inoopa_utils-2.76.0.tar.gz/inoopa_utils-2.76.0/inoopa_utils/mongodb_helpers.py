import os
from dotenv import load_dotenv
import pandas as pd
from pymongo.errors import OperationFailure
from pymongo import MongoClient, ASCENDING, TEXT
from concurrent.futures import ThreadPoolExecutor

from inoopa_utils.custom_types.decision_makers import DecisionMaker
from inoopa_utils.inoopa_logging import create_logger

load_dotenv()


class DbManagerMongo:
    """
    This class is used to manage the Mongo database.

    :param mongo_uri: The URI of the Mongo database to connect to.
    :param create_index_if_not_done: If the MongoDB indexes should be created if they don't exist.

    :attribute company_collection: The company collection object.
    :attribute do_not_call_me_collection: The do not call me collection object.
    :attribute decision_maker_collection: The decision maker collection object.
    :attribute legacy_co2_data_collection: The legacy co2 data collection object.
    :attribute legacy_decision_makers_collection: The legacy decision makers collection object.
    :attribute company_keywords: The company keywords collection object.

    :method update_do_not_call_me: Update the do_not_call_me collection in the database with a list of phone numbers.
    """

    def __init__(
        self,
        mongo_uri: str = os.environ["MONGO_READWRITE_PROD_URI"],
        create_index_if_not_done: bool = False,
        pretty_logging: bool = False,
    ):
        self._logger = create_logger("INOOPA_UTILS.DB_MANAGER.MONGO", pretty=pretty_logging)
        self._env = os.environ.get("ENV", "dev")

        _client = MongoClient(mongo_uri)
        _db = _client[self._env]

        self.company_collection = _db.get_collection("company")
        self.do_not_call_me_collection = _db.get_collection("do_not_call_me")
        self.decision_maker_collection = _db.get_collection("decision_maker")
        self.delivery_memory_collection = _db.get_collection("delivery_memory")
        self.legacy_co2_data_collection = _db.get_collection("legacy_co2_data")
        self.legacy_decision_makers_collection = _db.get_collection("legacy_decision_makers")
        self.phone_operators_cache_collection = _db.get_collection("phone_operators_cache")
        self.api_users_collection = _db.get_collection("api_users")
        self.company_keywords = _db.get_collection("company_keywords")
        if create_index_if_not_done:
            self._create_indexes()

    def update_do_not_call_me(self, phones: list[str]) -> None:
        """
        Method to update the do_not_call_me collection in the database.

        :param list[str]: The list of phone numbers to add to the do_not_call_me collection.
        """
        batch_size = 10_000
        phones_batch = [phones[i : i + batch_size] for i in range(0, len(phones), batch_size)]

        # We use a thread pool to update the database faster
        with ThreadPoolExecutor() as executor:
            executor.map(self._run_batch_update_do_not_call_me, phones_batch)
        self._logger.info(f"Updated {len(phones):_} phones in DoNotCallMe collection")

    def _run_batch_update_do_not_call_me(self, phone_batch: list[str]) -> None:
        """
        Method to update a chunk of the do_not_call_me collection in the database.

        :param updates: The list of DB update to execute.
        """
        batch_set = set(phone_batch)
        self._logger.info(f"Filtering {len(phone_batch)} phones...")
        existing_numbers = set(
            item["phone"] for item in self.do_not_call_me_collection.find({"phone": {"$in": list(batch_set)}})
        )
        new_numbers = [{"phone": number} for number in batch_set - existing_numbers]
        # Bulk insert new numbers
        if new_numbers:
            self._logger.info(f"Inserting {len(new_numbers)} new phones in collection...")
            self.do_not_call_me_collection.insert_many(new_numbers, ordered=False)
        else:
            self._logger.info("No new phones to insert found in batch")

    def _create_indexes(self) -> None:
        """Create the indexes in the Mongo database if they don't exist."""
        fields_to_index_legacy_co2_data = [
            [("_id", ASCENDING)],
            [("legacy_entity_id", ASCENDING)],
        ]
        fields_to_index_decision_makers = [
            [("company_id", ASCENDING)],
            [("legacy_entity_id", ASCENDING)],
            [("email", ASCENDING)],
            [("best_match", ASCENDING)],
            [("function_string", ASCENDING)],
            [("linkedin_url", ASCENDING)],
        ]
        fields_to_index_company = [
            [("address.string_address", ASCENDING)],
            [("address.region", ASCENDING)],
            [("address.postal_code", ASCENDING)],
            [("legal_form_type", ASCENDING)],
            [("best_website", ASCENDING)],
            [("best_website.website", ASCENDING)],
            [("best_email", ASCENDING)],
            [("best_phone", ASCENDING)],
            [("board_members.name", ASCENDING)],
            [("country", ASCENDING)],
            [("employee_category_code", ASCENDING)],
            [("establishments.name", ASCENDING)],
            [("name", ASCENDING)],
            [("status", ASCENDING)],
            [("name_text", TEXT)],
        ]
        legacy_fields_to_index_decision_makers = [
            [("company_id", ASCENDING)],
            [("email_score", ASCENDING)],
            [("phone_score", ASCENDING)],
            [("function_code", ASCENDING)],
            [("cluster", ASCENDING)],
            [("cluster_score", ASCENDING)],
            [("cluster_best_match", ASCENDING)],
            [("function_string", ASCENDING)],
        ]
        fields_to_index_company_keywords = [
            [("company_id", ASCENDING)],
        ]
        fields_to_index_delivery_memory = [
            [("company_id", ASCENDING)],
            [("best_phone.phone", ASCENDING)],
            [("best_email.email", ASCENDING)],
            [("best_website.website", ASCENDING)],
            [("delivery_date", ASCENDING)],
            [("decision_maker_ids", ASCENDING)],
        ]
        fields_to_index_phone_operators_cache = [
            [("operator", ASCENDING)],
            [("operator_last_update", ASCENDING)],
            [("last_update", ASCENDING)],
            [("_id", ASCENDING)],
        ]
        fields_to_index_do_no_call_me = [
            [("phone", ASCENDING)],
        ]
        self._logger.info("Creating indexes in collections (if not created yet)...")
        self._logger.info(
            "If this takes time (~10 mins), the indexes are not created yet. You will get a message when it's done."
        )

        collections_to_index = [
            {self.company_collection: fields_to_index_company},
            {self.decision_maker_collection: fields_to_index_decision_makers},
            {self.legacy_co2_data_collection: fields_to_index_legacy_co2_data},
            {self.legacy_decision_makers_collection: legacy_fields_to_index_decision_makers},
            {self.company_keywords: fields_to_index_company_keywords},
            {self.delivery_memory_collection: fields_to_index_delivery_memory},
            {self.do_not_call_me_collection: fields_to_index_do_no_call_me},
            {self.phone_operators_cache_collection: fields_to_index_phone_operators_cache},
        ]

        for indexer in collections_to_index:
            for collection, fields in indexer.items():
                for index in fields:
                    self._logger.debug(f"Creating index {index} in `{collection.name}` collection...")
                    try:
                        if index[0][0] != "_id":
                            collection.create_index(index, background=True)
                        else:
                            collection.create_index(index)
                    # Skip if index already exists
                    except OperationFailure as ex:
                        print(ex)
                        continue
        self._logger.info("Indexes created in all collections")

    def add_decision_makers_to_company(
        self, company_id: str, only_decision_makers_with_email: bool = False
    ) -> list[DecisionMaker]:
        """
        Add decision makers to companies list of dicts.

        :param companies: List of dicts containing companies data.
            Each company should contains a key `_id` or `registered_number`.
        :return: the list of decision makers objects.
        """
        self._logger.debug(f"Adding decision makers to company: {company_id}")
        filters: dict = {"company_id": company_id}
        if only_decision_makers_with_email:
            filters["email"] = {"$nin": [None, ""]}
        decision_makers = self.decision_maker_collection.find(filters)
        if decision_makers:
            decision_makers = [DecisionMaker(**decision_maker) for decision_maker in decision_makers]
            self._logger.info(f"Found {len(decision_makers)} decision makers for company: {company_id}")
            return decision_makers

        self._logger.debug(f"No decision makers found for company: {company_id}")
        return []


def enrich_companies_df_with_decision_makers(
    companies_df: pd.DataFrame, db_manager: DbManagerMongo | None = None, only_decision_makers_with_email: bool = False
) -> pd.DataFrame:
    """
    Add decision makers to a companies dataframe.

    :param companies_df: The companies dataframe to enrich. Should contain a column `__id` or `registered_number`.
    :return: The companies dataframe with the decision makers added.
        If multiple decision makers are found for one company, will create multiple rows for the company.
    """
    if companies_df.empty:
        return companies_df
    if db_manager is None:
        db_manager = DbManagerMongo()
    db_manager._logger.info("Adding decision makers to companies dataframe...")
    if "_id" in companies_df.columns:
        id_column = "_id"
    elif "registration_number" in companies_df.columns:
        id_column = "registration_number"
    else:
        raise ValueError("The companies dataframe should contain a column `_id` or `registered_number`.")

    companies_ids = list(set(companies_df[id_column].to_list()))
    db_manager._logger.info(f"counting companies with decision makers: {len(companies_ids)}")

    filters = {"company_id": {"$in": companies_ids}}
    if only_decision_makers_with_email:
        filters["email"] = {"$nin": [None, ""]}

    companies_with_dms_ids = db_manager.decision_maker_collection.find(filters, {"_id": 0, "company_id": 1})
    companies_with_dms_ids = set([company["company_id"] for company in companies_with_dms_ids])

    db_manager._logger.info(f"Found {len(companies_with_dms_ids)} companies with decision makers")

    new_rows = []
    for i, row in companies_df.iterrows():
        if row[id_column] not in companies_with_dms_ids:
            continue
        decision_makers = db_manager.add_decision_makers_to_company(row[id_column], only_decision_makers_with_email)
        if not decision_makers:
            continue
        else:
            # If there are multiple decision makers, create a new row for each one
            for y, decision_maker in enumerate(decision_makers):
                if y == 0:
                    # Update the original row with the first decision maker's information
                    companies_df.at[i, "decision_maker_firstname"] = decision_maker.firstname
                    companies_df.at[i, "decision_maker_lastname"] = decision_maker.lastname
                    companies_df.at[i, "decision_maker_email"] = decision_maker.email
                    companies_df.at[i, "decision_maker_language"] = decision_maker.language
                    companies_df.at[i, "decision_maker_function_cluster"] = decision_maker.cluster
                else:
                    # Create new rows for additional decision makers
                    new_row = row.copy()
                    new_row["decision_maker_firstname"] = decision_maker.firstname
                    new_row["decision_maker_lastname"] = decision_maker.lastname
                    new_row["decision_maker_email"] = decision_maker.email
                    new_row["decision_maker_language"] = decision_maker.language
                    new_row["decision_maker_function_cluster"] = decision_maker.cluster
                    new_rows.append(new_row)

    if new_rows:
        companies_df = pd.concat([companies_df, pd.DataFrame(new_rows)], ignore_index=True)
    # make sure the companies are displayed in the same order as the original dataframe
    return companies_df.sort_values(by=id_column)


def enrich_companies_dicts_with_decision_makers(
    companies_dicts: list[dict], db_manager: DbManagerMongo | None = None
) -> list[dict]:
    """
    Add decision makers to a companies list of dicts.

    :param companies_dicts: List of dicts containing companies data.
        Each company should contains a key `_id` or `registered_number`.
    :return: the list of companies dicts with the decision makers added under the `decision_makers` key.
    """
    if db_manager is None:
        db_manager = DbManagerMongo()
    db_manager._logger.info("Adding decision makers to companies dicts...")
    for i, company_dict in enumerate(companies_dicts):
        decision_makers = db_manager.add_decision_makers_to_company(company_dict["_id"])
        companies_dicts[i]["decision_makers"] = []

        if not decision_makers:
            continue

        for dm in decision_makers:
            companies_dicts[i]["decision_makers"].append(
                {
                    "firstname": dm.firstname,
                    "lastname": dm.lastname,
                    "email": dm.email,
                    "language": dm.language,
                    "function_cluster": dm.cluster,
                }
            )

    return companies_dicts


if __name__ == "__main__":
    os.environ["ENV"] = "prod"
    db_manager = DbManagerMongo(create_index_if_not_done=True)
