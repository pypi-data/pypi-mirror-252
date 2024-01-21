from circles_local_database_python.generic_mapping import GenericMapping
from logger_local.Logger import Logger
from phonenumbers import (NumberParseException, PhoneNumberFormat,
                          format_number, parse)

from .phone_local_constans import code_object_init

logger = Logger.create_logger(object=code_object_init)


class PhonesLocal(GenericMapping):
    def __init__(self) -> None:
        super().__init__(default_schema_name="phone",
                         default_table_name="phone_table",
                         default_view_table_name="phone_view",
                         default_id_column_name="phone_id")

    def get_normalized_phone_number_by_phone_id(self, phone_id: int) -> int:
        logger.start(object={"phone_id": phone_id})
        data = self.select_one_dict_by_id(select_clause_value="local_number_normalized",
                                          id_column_value=phone_id)
        if not data:
            logger.end("No phone number found for phone_id " +
                       str(phone_id))
        else:
            phone_number = int(data["local_number_normalized"])
            logger.end("Return Phone Number of a specific phone id",
                       object={'phone_number': phone_number})
            return phone_number  # TODO: should we add area_code?

    def verify_phone_number(self, phone_number: int) -> None:
        logger.start(object={"phone_number": phone_number})
        self.update_by_id(id_column_value=phone_number,
                          data_json={"is_verified": 1})
        logger.end()

    def is_verified(self, phone_number: int) -> bool:
        logger.start(object={"phone_number": phone_number})
        data = self.select_one_dict_by_id(select_clause_value="is_verified",
                                          id_column_value=phone_number)
        if not data:
            logger.end("No phone number found for phone_number " +
                       str(phone_number))
            return False
        is_verified = data["is_verified"]
        logger.end("Return is_verified of a specific phone id",
                   object={'is_verified': is_verified})
        return is_verified

    @staticmethod
    def normalize_phone_number(original_number: str, region: str) -> dict:
        """
        Normalize phone number to international format.
        :param original_number: Original phone number.
        :param region: Region of the phone number.
        :return: Dictionary with the normalized phone number and the international code.

        Example:
        original_number = "0549338666"
        region = "IL"
        result = {
            "international_code": 972,
            "full_number_normalized": "+972549338666"
        }
        """
        try:
            parsed_number = parse(original_number, region)
            international_code = parsed_number.country_code
            full_number_normalized = format_number(
                parsed_number, PhoneNumberFormat.E164)
            number_info = {
                "international_code": international_code,
                "full_number_normalized": full_number_normalized
            }
            return number_info
        except NumberParseException as e:
            logger.error(
                f"Invalid phone number: {original_number}. Exception: {str(e)}")

    def process_phone(self, original_phone_number: str, contact_id: int = None) -> dict:
        """
        Process phone number and return normalized phone number.
        :param original_phone_number: Original phone number.
        :param contact_id: Contact id.
        :return: Dictionary with the normalized phone number and the international code.
        """
        logger.start(object={'original_phone_number': original_phone_number})
        self.set_schema(schema_name='location_profile')
        profile_id = logger.user_context.get_effective_profile_id()
        location_id = self.select_one_tuple_by_id(view_table_name='location_profile_view', select_clause_value='location_id',
                                                  id_column_name='profile_id', id_column_value=profile_id)[0]
        if location_id is None:
            logger.error(
                f"profile {profile_id} location is not set phone number will cannot normalized")
            return None
        self.set_schema(schema_name='location')
        country_id = self.select_one_tuple_by_id(view_table_name='location_view',  select_clause_value='country_id',
                                                 id_column_name='location_id', id_column_value=location_id)[0]
        country_iso_code = self.select_one_tuple_by_id(view_table_name='country_ml_view', select_clause_value='iso',
                                                       id_column_name='country_id', id_column_value=country_id)[0]
        normalized_phone_number = self.normalize_phone_number(
            original_number=original_phone_number, region=country_iso_code)
        phone_data = {
            'number_original': original_phone_number,
            'international_code': normalized_phone_number['international_code'],
            'full_number_normalized': normalized_phone_number['full_number_normalized'],
            'local_number_normalized': int(str(normalized_phone_number['full_number_normalized'])
                                           .replace(str(normalized_phone_number['international_code']), '')),
            'created_user_id': logger.user_context.get_effective_user_id(),
        }
        self.set_schema(schema_name='phone')
        phone_id = self.insert(data_json=phone_data)

        self.set_schema(schema_name='phone_profile')
        # link phone to profile
        phone_profile_id = self.insert_mapping(
            entity_name1='phone', entity_name2='profile', entity_id1=phone_id, entity_id2=profile_id)

        # link phone to contact
        if contact_id is not None:
            self.set_schema(schema_name='contact_phone')
            contact_phone_id = self.insert_mapping(
                entity_name1='contact', entity_name2='phone', entity_id1=contact_id, entity_id2=phone_id)

        result = {
            'phone_profile_id': phone_profile_id,
            'phone_id': phone_id,
            'normalized_phone_number': normalized_phone_number,
            'original_phone_number': original_phone_number,
            'contact_phone_id': contact_phone_id if contact_id is not None else None,
        }
        logger.end("success processing phone number", object=result)
        return result
