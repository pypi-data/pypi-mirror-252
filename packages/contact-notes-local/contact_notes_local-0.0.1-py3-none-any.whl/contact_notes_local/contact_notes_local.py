from .contact_notes_local_constants import CONTACT_NOTES_PYTHON_PACKAGE_CODE_LOGGER_OBJECT
from database_mysql_local.generic_mapping import GenericMapping
from language_remote.lang_code import LangCode
from logger_local.LoggerLocal import Logger
from text_block_local.text_block import TextBlocks
from database_infrastructure_local.number_generator import NumberGenerator

DEFAULT_SCHEMA_NAME = "contact_note"
DEFAULT_TABLE_NAME = "contact_note_text_block_table"
DEFAULT_VIEW_NAME = "contact_note_text_block_view"
DEFAULT_ID_COLUMN_NAME = "conact_note_text_block_id"
DEFAULT_ENTITY_NAME1 = "contact_note"
DEFAULT_ENTITY_NAME2 = "text_block"


class ContactNotesLocal(GenericMapping):
    def __init__(self, default_schema_name: str = DEFAULT_SCHEMA_NAME,
                 default_table_name: str = DEFAULT_TABLE_NAME,
                 default_view_table_name: str = DEFAULT_VIEW_NAME,
                 default_id_column_name: str = DEFAULT_ID_COLUMN_NAME,
                 default_entity_name1: str = DEFAULT_ENTITY_NAME1,
                 default_entity_name2: str = DEFAULT_ENTITY_NAME2,
                 lang_code: LangCode = None, is_test_data: bool = False) -> None:
        super().__init__(default_schema_name=default_schema_name,
                         default_table_name=default_table_name,
                         default_view_table_name=default_view_table_name,
                         default_id_column_name=default_id_column_name,
                         default_entity_name1=default_entity_name1,
                         default_entity_name2=default_entity_name2,
                         is_test_data=is_test_data)
        self.logger = Logger.create_logger(object=CONTACT_NOTES_PYTHON_PACKAGE_CODE_LOGGER_OBJECT)
        self.lang_code = lang_code or self.logger.user_context.get_effective_profile_preferred_lang_code()
        self.text_blocks = TextBlocks()

    def insert_contact_notes(self, contact_dict: dict, contact_id: int, ignore_duplicate: bool = False) -> int:
        self.logger.start(object={"contact_dict": contact_dict, "contact_id": contact_id,
                                  "ignore_duplicate": ignore_duplicate})
        note = contact_dict.get('notes', None)
        random_number = NumberGenerator.get_random_number(schema_name=self.schema_name,
                                                          view_name="contact_note_table")
        if not note:
            self.logger.end(f"no note for contact_id: {contact_id}")
            return None
        data_json = {
            'contact_id': contact_id,
            'note': note,
            'number': random_number,
            'identifier': None,         # TODO: what is this?
            # TODO: shall we add created_user_id?
            # TODO: shall we add created_real_user_id?
            # TODO: shall we add created_effective_profile_id? 
        }
        contact_note_id = self.insert(table_name="contact_note_table", data_json=data_json, ignore_duplicate=ignore_duplicate)
        self.logger.end(object={"contact_note_id": contact_note_id})
        return contact_note_id

    # TODO: when we have contact_note_view ready, we can test the following method and use it
    '''
    def select_multi_dict_by_contact_id(self, contact_id: int) -> dict:
        self.logger.start(object={"contact_id": contact_id})
        contact_note_dict = self.select_multi_dict_by_id(view_table_name="contact_note_table",
                                                         id_column_name="contact_id",
                                                         id_column_value=contact_id)
        self.logger.end(object={"contact_note_dict": contact_note_dict})
        return contact_note_dict
    '''

    def delete_by_contact_id(self, contact_id: int) -> None:
        self.logger.start(object={"contact_id": contact_id})
        super().delete_by_id(table_name="contact_note_table", id_column_name='contact_id', id_column_value=contact_id)
        self.logger.end()

    def insert_contact_note_text_block_table(self, contact_note_id: int, note: str) -> int:
        '''
        This method will insert the note into the contact_note_text_block_table if it not exists there
        :param contact_note_id: the id of the contact_note_table
        :param note: the note to be inserted
        :return: the id of the inserted row
        '''
        self.logger.start(object={"contact_note_id": contact_note_id, "note": note})
        if not note:
            self.logger.end(log_message=f"no note for contact_note_id", object={"contact_note_id": contact_note_id})
            return None
        # Check if the contact_note is already linked to text_blocks
        mapping_tuple = self.select_multi_tuple_by_id(view_table_name=self.default_view_table_name,
                                                      id_column_name="contact_note_id",
                                                      id_column_value=contact_note_id)
        # TODO: shall we keep this check?
        if mapping_tuple:
            self.logger.end(log_message=f"contact_note_id: {contact_note_id} already linked to text_blocks",
                            object={"contact_note_id": contact_note_id})
            return None
        text_blocks_list = self.get_text_blocks_list_from_note(note=note)

        text_block_ids_list = []
        conact_note_text_block_ids_list = []
        for i, text_block in enumerate(text_blocks_list):
            data_json = {
                'text': text_block,
                'seq': i,  # This is the index of the current text_block in the list
            }
            text_block_id = self.text_blocks.insert(schema_name="text_block", table_name="text_block_table",
                                                    data_json=data_json)
            text_block_ids_list.append(text_block_id)
            self.text_blocks.process_text_block_by_id(text_block_id=text_block_id)

            # link the contact_note_id to the text_block_id
            data_json = {
                'contact_note_id': contact_note_id,
                'text_block_id': text_block_id,
                'seq': i
            }
            # TODO: check if self.set_schema(schema_name=DEFAULT_SCHEMA_NAME) is actually necessary
            self.set_schema(schema_name=DEFAULT_SCHEMA_NAME)
            # Insert the mapping between the contact_note_id and the text_block_id
            self.logger.info(log_message=f"Inserting mapping between contact_note_id: {contact_note_id} and"
                             f" text_block_id: {text_block_id}")
            conact_note_text_block_id = self.insert_mapping(entity_name1=DEFAULT_ENTITY_NAME1,
                                                            entity_name2=DEFAULT_ENTITY_NAME2,
                                                            entity_id1=contact_note_id,
                                                            entity_id2=text_block_id)
            conact_note_text_block_ids_list.append(conact_note_text_block_id)
        self.logger.end(object={"contact_note_id": contact_note_id, "text_block_ids_list": text_block_ids_list,
                                "conact_note_text_block_ids_list": conact_note_text_block_ids_list})
        return conact_note_text_block_ids_list

    def get_text_blocks_list_from_note(self, note: str) -> list:
        self.logger.start(object={"note": note})
        text_blocks_list = note.split("\n")
        self.logger.end(object={"text_blocks_list": text_blocks_list})
        return text_blocks_list
