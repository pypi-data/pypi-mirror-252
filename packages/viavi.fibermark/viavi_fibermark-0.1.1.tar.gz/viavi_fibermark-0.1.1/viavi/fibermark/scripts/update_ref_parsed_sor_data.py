# from os import listdir
# from os.path import isfile, join
# from pathlib import Path

# from viavi.fibermark.db_utils.connect import prod_db_session
# from viavi.fibermark.db_utils.db_insertion import upsert_measure, upsert_parsed_sor_data
# from viavi.fibermark.utils.helpers import try_parsing_sor_data

# if __name__ == "__main__":
#     directory_to_import = "/home/aboussejra/inspect/Prof_v3_updated_storage/"
#     list_files_directory = [
#         directory_to_import + file for file in listdir(directory_to_import) if isfile(join(directory_to_import, file))
#     ]
#     sor_datas = [try_parsing_sor_data(sor_file) for sor_file in list_files_directory]
#     for sor_data in sor_datas:
#         ref_id = int(Path(sor_data.filename).stem)
#         upsert_parsed_sor_data(prod_db_session, ref_id, sor_data)
#         upsert_measure(prod_db_session, "reference", ref_id, sor_data)
#         # Need to automatize remote upload file too
#         prod_db_session.commit()
# NOT PERFEECT, USE DUMP currently
