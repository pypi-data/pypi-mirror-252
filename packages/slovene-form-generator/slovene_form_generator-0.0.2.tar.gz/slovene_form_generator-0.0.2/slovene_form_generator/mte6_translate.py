from collections import defaultdict as dd

class Mte6Translate:

    def __init__(self):
        self.mte6_dict_en_to_sl = dd()
        self.mte6_dict_sl_to_en = dd()

        file_with_msd_translations = open("mte_6_dict_sl_en.tsv", "r", encoding="UTF-8").readlines()

        for line in file_with_msd_translations[1:]:  # SKIP HEADERS
            msd_en,\
            features_en,\
            msd_sl,\
            features_sl,\
            types,\
            tokens,\
            examples = line.strip("\n").split("\t")

            self.mte6_dict_sl_to_en[msd_sl] = msd_en
            self.mte6_dict_en_to_sl[msd_en] = msd_sl

    def msd_en_to_sl(self, msd_en):
        """FUNCTION - Translate MSD_EN to MSD_SL"""
        return self.mte6_dict_en_to_sl[msd_en]

    def msd_sl_to_en(self, msd_sl):
        """FUNCTION - Translate MSD_SL to MSD_EN"""
        return self.mte6_dict_sl_to_en[msd_sl]
