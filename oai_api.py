# -*- coding: utf-8 -*-

import re
from random import randint
from sickle import Sickle

# http://pbc.gda.pl/dlibra/doczip?id=24617


class LibraryCrawler(object):

    """
    Perform a library scan over specific types of documents
    and return first matching record. Page from which the
    query starts is random.
    """

    def __init__(self, logger, config, query):
        self.logger = logger
        oai_api_url = config['default']['oai_api_url']
        self.sickle = Sickle(oai_api_url)
        self.resumption_token = self.get_token()

        # Queried attribute. I.e. type, description, format, subject, etc.
        self.query_dict = query

    def get_token(self):
        query = self.sickle.ListRecords(
            metadataPrefix='oai_dc',
            set='dLibraDigitalLibrar:PartnersResources:BGPAN'
        )
        return query.resumption_token

    def query_itarator(self):
        length = self.resumption_token.complete_list_size
        rand_num = randint(20, int(length))
        new_token = re.sub(
            '_DL_LAST_ITEM_\d+_DL_', '_DL_LAST_ITEM_%d_DL_' % rand_num,
            self.resumption_token.token
        )
        return self.sickle.ListRecords(resumptionToken=new_token)

    @staticmethod
    def is_small_enough(description):
        try:
            for item in description:
                match = re.search(r"([0-9]+)\ss\.", item)
                if match:
                    pages = int(match.groups()[0])
                    if pages > 250:
                        return False

        except IndexError:
            pass
        return True

    def run(self):
        found = False
        iterator = self.query_itarator()
        while not found:
            record = iterator.next()
            for key, values in self.query_dict.items():
                try:
                    attribute = record.metadata[key]
                    description = record.metadata['description']
                    if attribute[0] in values and self.is_small_enough(description):
                        self.logger.info('Found something interesting!')
                        self.logger.info(record.metadata)
                        found = True
                        content_id = record.metadata['identifier'][1].lstrip('oai:pbc.gda.pl:')
                        return record, content_id
                except (KeyError, AttributeError):
                    pass
        return None, None
