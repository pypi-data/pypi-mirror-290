import json
from logger_local.LoggerLocal import Logger
from database_mysql_local.generic_crud_ml import GenericCRUDML
from database_mysql_local.generic_crud import GenericCRUD
from phones_local.phones_local import PhonesLocal
from profile_local.profiles_local import ProfilesLocal
from message_local.MessageChannels import MessageChannel
from message_local.ChannelProviderConstants import INFORU_MESSAGE_PROVIDER_ID

from .WhatsAppLocalConstants import get_logger_object
from .WhatsAppMessageInforuLocal import WhatsAppMessageInforuLocal

# TODO (future) Can we get those from general file? Can we generate those in the future using Sql2Code?
TEST_API_TYPE_ID = 4
INFORU_WHATSAPP_SYSTEM_ID = 8
INFORU_WHATAPP_PUSH_API_TYPE_ID = 20

logger_object = get_logger_object()
logger = Logger.create_logger(object=logger_object)


def insertMessageRecievedToTheDatabase(request_parameters_dict: dict) -> list[int]:
    """Read parameters from the payload and insert them"""
    logger.start(object={"request_parameters": request_parameters_dict})
    message_generic_crud_ml_instance = GenericCRUDML(default_schema_name="message", default_table_name="message_table")
    message_inforu_generic_crud_ml_instance = GenericCRUDML(
        default_schema_name="message", default_table_name="message_inforu_table")

    extract_result_list = __extract_message_data(request_parameters_dict)
    messages_ids_list: list = []
    messages_inforu_ids_list: list = []
    for extract_result in extract_result_list:
        message_dict, message_inforu_dict = extract_result
        message_id = message_generic_crud_ml_instance.insert(
            schema_name="message", table_name="message_table",
            data_dict=message_dict)
        if message_id is not None:
            logger.info("Message inserted successfully", object={"message_id": message_id})
            messages_ids_list.append(message_id)
        message_inforu_dict["message_id"] = message_id
        message_inforu_id = message_inforu_generic_crud_ml_instance.insert(
            schema_name="message", table_name="message_inforu_table", data_dict=message_inforu_dict)
        if message_inforu_id is not None:
            logger.info("Message inforu inserted successfully", object={"message_inforu_id": message_inforu_id})
            messages_inforu_ids_list.append(message_inforu_id)
    if len(messages_ids_list) == 0:
        raise Exception("Message/Messages were not created")
    result_message = {"message": "Message/Messages created successfully", "messages_ids_list": messages_ids_list,
                      "messages_inforu_ids_list": messages_inforu_ids_list}
    logger.end(object={"result_message": result_message})
    return result_message

"""
Example of request_parameters:
{
    "CustomerId":28132,
    "ProjectId":1042593,
    "Data":[
        {
            "Channel":"SMS_MO",
            "Type":"PhoneNumber",
            "Value":"0522222229",
            "Keyword":"wt1",
            "Message":"wt1 ",
            "Network":"WhatsApp",
            "ShortCode":"+97233769182",
            "ApplicationID":"11542",
            "CustomerParam":"SMf14104210035723ecab943567b4ad4b5",
            "MoSessionId":"SMf14104210035723ecab943567b4ad4b5"
        }
    ]
}
"""
#TODO (future)Move the inforu parts of this method to __extract_message_inforu_data(request_parameters_dict: dict) -> list [dict]:
def __extract_message_data(request_parameters_dict: dict) -> list[dict, dict]:
    """Extract message data from the payload"""
    logger.start(object={"request_parameters": request_parameters_dict})
    result_list:  list = []
    message_customer_id = request_parameters_dict.get("CustomerId")
    message_project_id = request_parameters_dict.get("ProjectId")
    phones_local = PhonesLocal()
    profiles_local = ProfilesLocal()

    request_parameters_data: list[dict] = request_parameters_dict.get("Data")
    if not request_parameters_data:
        logger.end(object={"result_list": result_list})
        return []
    for request_parameters_data_item in request_parameters_data:
        message_data: dict = {}
        message_inforu_dict: dict = {}
        message_inforu_dict["inforu_customer_id"] = message_customer_id
        message_inforu_dict["inforu_project_id"] = message_project_id
        message_inforu_dict["inforu_type"] = request_parameters_data_item.get("Type")
        message_data["body"] = request_parameters_data_item.get("Message")
        message_inforu_dict["inforu_channel"] = request_parameters_data_item.get("Channel")
        message_data["actual_channel_id"] = MessageChannel.WHATSAPP.value
        message_data["from_provider_id"] = INFORU_MESSAGE_PROVIDER_ID
        message_data["from_user_external_id"] = get_user_external_id_by_api_type_and_request_parameter(
            api_type_id=INFORU_WHATAPP_PUSH_API_TYPE_ID, request_parameters_dict=request_parameters_dict
        )
        message_data["from_api_type_id"] = INFORU_WHATAPP_PUSH_API_TYPE_ID
        message_inforu_dict["inforu_network"] = request_parameters_data_item.get("Network")
        message_inforu_dict["inforu_incoming_json"] = json.dumps(request_parameters_dict)
        receiver_phone_number = request_parameters_data_item.get("ShortCode")
        message_inforu_dict["inforu_short_code"] = receiver_phone_number
        message_inforu_dict["inforu_application_id"] = request_parameters_data_item.get("ApplicationID")
        message_inforu_dict["inforu_customer_param"] = request_parameters_data_item.get("CustomerParam")
        message_inforu_dict["inforu_mo_session_id"] = request_parameters_data_item.get("MoSessionId")
        message_inforu_dict["inforu_keyword"] = request_parameters_data_item.get("Keyword")
        sender_phone_number = request_parameters_data_item.get("Value")
        message_inforu_dict["inforu_value"] = sender_phone_number
        logger.info("Normalizing the sender phone number " + sender_phone_number,
                    object={"sender_phone_number": sender_phone_number})
        number_info = PhonesLocal.normalize_phone_number(original_number=sender_phone_number, region="IL")
        sender_normalized_phone_number = number_info.get("full_number_normalized")
        # Replace the leading 0 in the phone number by 972 if there's a leading 0
        if sender_normalized_phone_number.startswith("0"):
            sender_normalized_phone_number = "972" + sender_normalized_phone_number[1:]
            logger.info("Normalized sender phone number " + sender_normalized_phone_number,
                        object={"sender_normalized_phone_number": sender_normalized_phone_number})
        sender_phone_id = phones_local.get_phone_id_by_full_number_normalized(
            full_number_normalized=sender_normalized_phone_number)
        # Get Sender profile id
        sender_profile_id = profiles_local.select_one_value_by_column_and_value(
            select_clause_value="profile_id", column_name="main_phone_id", column_value=sender_phone_id
        )
        if sender_profile_id is None:
            # Create and insert a new profile
            profile_dict = {
                "profile.name":  sender_phone_number,
            }
            sender_profile_id = profiles_local.insert(profile_dict=profile_dict)
        message_data["sender_profile_id"] = sender_profile_id
        # Get receiver normalized phone number
        logger.info("Normalizing the receiver phone number " + receiver_phone_number,
                    object={"receiver_phone_number": receiver_phone_number})
        number_info = PhonesLocal.normalize_phone_number(
            original_number=receiver_phone_number, region="IL")
        receiver_normalized_phone_number = number_info.get("full_number_normalized")
        logger.info("Normalized receiver phone number " + receiver_normalized_phone_number,
                    object={"receiver_normalized_phone_number": receiver_normalized_phone_number})
        # Remove leading #
        if receiver_normalized_phone_number.startswith("#"):
            receiver_normalized_phone_number = receiver_normalized_phone_number[1:]

        # Get receiver phone id
        receiver_phone_id = phones_local.get_phone_id_by_full_number_normalized(full_number_normalized=receiver_phone_number)
        # Get receiver profile id
        receiver_profile_id = profiles_local.select_one_value_by_column_and_value(
            select_clause_value="profile_id", column_name="main_phone_id", column_value=receiver_phone_id
        )
        message_data["to_profile_id"] = receiver_profile_id
        result_list.append((message_data, message_inforu_dict))

    logger.end(object={"result_list": result_list})
    return result_list


def get_user_external_id_by_api_type_and_request_parameter(api_type_id: int, request_parameters_dict: dict) -> int:
    logger.start(object={"api_type_id": api_type_id, "request_parameters": request_parameters_dict})
    user_external_generic_crud = GenericCRUD(
        default_schema_name="user_external", default_view_table_name="user_external_view")
    user_external_id = None
    if api_type_id == TEST_API_TYPE_ID:
        user_external_generic_crud.is_test_data = True
    if api_type_id == INFORU_WHATAPP_PUSH_API_TYPE_ID or api_type_id == TEST_API_TYPE_ID:
        inforu_customer_id = request_parameters_dict.get("CustomerId")
        inforu_project_id = request_parameters_dict.get("ProjectId")
        # TODO: When we have redis then we can select with JSON_EXTRACT

        user_external_table = user_external_generic_crud.select_one_dict_by_where(
            select_clause_value="user_external_id, system_id, username",
            where="system_id=%s AND customer_id=%s AND project_id=%s",
            params=(INFORU_WHATSAPP_SYSTEM_ID, inforu_customer_id, inforu_project_id))
        user_external_id = user_external_table.get("user_external_id")
        if user_external_id is None:
            logger.exception(object={"user_external_id": user_external_id, "customer_id": inforu_customer_id,
                                     "project_id": inforu_project_id})
            raise Exception("User external id not found")
        logger.end(object={"user_external_id": user_external_id,
                           "user_external_generic_crud.is_test_data": user_external_generic_crud.is_test_data})
        return user_external_id
    else:
        logger.exception(object={"api_type_id": api_type_id})
        raise Exception("Invalid API type id")

# @handler_decorator(logger)
# def deleteHandler(request_parameters: dict) -> dict:
#     """url/5   (5 is the eventId)"""

#     message_id = request_parameters.get('eventId')
#     is_test_data = request_parameters.get("isTestData", False)
#     MessageLocal().delete_by_message_id(message_id=message_id)
#     message = {"message": "Message deleted successfully"}
#     return message


# TODO This should be imported from entity-type-python-package (this file will be generated by Sql2Code)
# @handler_decorator(logger)
# def getAllHandler(request_parameters: dict) -> list:
#     """url?langCode=en&limit=10"""

#     lang_code_str = request_parameters.get("langCode") or DEFAULT_LANG_CODE_STR
#     limit = request_parameters.get("limit")
#     is_test_data = request_parameters.get("isTestData", False)
#     messages_list = MessageLocal().select_all_messages(lang_code_str, limit=limit)
#     return messages_list


# @handler_decorator(logger)
# def getMessageByProfileIdHandler(request_parameters: dict) -> list:
#     """url/5?limit=10   (5 is the profileId)"""

#     request_parameters = request_parameters
#     profile_id = request_parameters.get("profileId")
#     limit = request_parameters.get("limit")

#     is_test_data = request_parameters.get("isTestData", False)
#     messages_list = MessageLocal().select_messages_by_profile_id(profile_id, limit=limit)
#     return messages_list


# @handler_decorator(logger)
# def getMessageByeventIdHandler(request_parameters: dict) -> dict:
#     """url/5?isTestData=true   (eventId)"""

#     message_id = request_parameters.get("eventId")

#     is_test_data = request_parameters.get("isTestData", False)
#     message = MessageLocal().select_by_message_id(message_id)
#     if not message:
#         raise Exception(f"Message not found with message_id: {message_id}")
#     return message


# @handler_decorator(logger)
# def updateHandler(request_parameters: dict) -> dict:
#     """url/5  (eventId)
#     Read parameters from the payload and update them"""

#     message_id = request_parameters.get('eventId')
#     is_test_data = request_parameters.get("isTestData", False)
#     if not message_id:
#         raise Exception("message_id is required")

#     MessageLocal().update_by_message_id(message_id, request_parameters)
#     message = {"message": "Message updated successfully"}
#     return message


# @handler_decorator(logger)
# def getMessageByMessageTitleHandler(request_parameters: dict) -> list:  # TODO: test
#     """url/SomeTitle?limit=10"""

#     title = request_parameters.get("title")

#     limit = request_parameters.get("limit")
#     is_test_data = request_parameters.get("isTestData", False)
#     messages_list = MessageLocal().select_events_by_title(title, limit=limit)
#     return messages_list
