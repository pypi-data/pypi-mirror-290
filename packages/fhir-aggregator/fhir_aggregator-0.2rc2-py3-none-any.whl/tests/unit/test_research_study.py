import json


from fhir_aggregator.client import ResearchStudySummary


def test_dbgap_research_study():
    """Query dbGap server."""
    from pprint import pprint
    with open('tests/fixtures/dbgap_research_study.json') as fp:
        research_study = json.load(fp)

        assert research_study
        assert isinstance(research_study, dict)
        dbgap_research_study_summary = ResearchStudySummary(research_study=research_study)
        pprint(dbgap_research_study_summary.research_study['extension'])
        assert dbgap_research_study_summary
        extensions = dbgap_research_study_summary.extensions
        assert len(extensions) == 17
        pprint(extensions)
        assert set(extensions) == set(
            {'research_study_citers_citer_title': 'Integrative genomic analysis of the '
                                                  'human immune response to influenza '
                                                  'vaccination',
             'research_study_citers_citer_url': 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3713456',
             'research_study_computed_ancestry_ancestry_count_ancestry': 'LEN',
             'research_study_computed_ancestry_ancestry_count_count': 7,
             'research_study_content_num_analyses': 0,
             'research_study_content_num_documents': 0,
             'research_study_content_num_molecular_datasets': 1,
             'research_study_content_num_phenotype_datasets': 3,
             'research_study_content_num_samples': 246,
             'research_study_content_num_sub_studies': 0,
             'research_study_content_num_subjects': 246,
             'research_study_content_num_variables': 30,
             'research_study_molecular_data_types_molecular_data_type': 'SNP Genotypes '
                                                                        '(Array)',
             'research_study_release_date': '2017-06-02',
             'research_study_study_consents_study_consent': 'GRU-IRB',
             'research_study_study_markersets_study_markerset': 'HumanOmniExpress-12v1_A',
             'research_study_study_overview_url': 'https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs000635.v1.p1'}
        )
        print(dbgap_research_study_summary.simplified)
        assert dbgap_research_study_summary.simplified == {'identifier': 'phs000635.v1.p1',
                                                           'resourceType': 'ResearchStudy', 'id': 'phs000635',
                                                           'title': 'Adult Influenza Vaccine Genetics',
                                                           'status': 'completed',
                                                           'description': '\nThis study includes two cohorts composed of healthy adults immunized with seasonal influenza vaccine. The first cohort was composed exclusively of males and second of females. Enrollment was restricted to individuals of European heritage to simplify the genetic analysis. Serum samples were collected prior to immunization and at 14 days and 28 days post immunization. Anti-hemagglutinin and neutralizing antibody activity was measured at each of the three time points for Influenza H1N1, H3N2, and Influenza B strains corresponding to the content of the vaccine. Peripheral blood RNA (PaxGene) were collected before immunization and on days 1, 3, and 14 post immunization. The RNA samples were analyzed using Illumina Human HT-12 v3 (Cohort 1) and Illumina HT-12 v4 beadarrays (Cohort 2).\n',
                                                           'meta': 'U', 'category': 'Prospective Longitudinal Cohort',
                                                           'focus': 'D007251', 'condition': 'C0021400',
                                                           'keyword': 'C0021400',
                                                           'research_study_study_overview_url': 'https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs000635.v1.p1',
                                                           'research_study_release_date': '2017-06-02',
                                                           'research_study_study_consents_study_consent': 'GRU-IRB',
                                                           'research_study_content_num_phenotype_datasets': 3,
                                                           'research_study_content_num_molecular_datasets': 1,
                                                           'research_study_content_num_variables': 30,
                                                           'research_study_content_num_documents': 0,
                                                           'research_study_content_num_analyses': 0,
                                                           'research_study_content_num_subjects': 246,
                                                           'research_study_content_num_samples': 246,
                                                           'research_study_content_num_sub_studies': 0,
                                                           'research_study_computed_ancestry_ancestry_count_ancestry': 'LEN',
                                                           'research_study_computed_ancestry_ancestry_count_count': 7,
                                                           'research_study_study_markersets_study_markerset': 'HumanOmniExpress-12v1_A',
                                                           'research_study_molecular_data_types_molecular_data_type': 'SNP Genotypes (Array)',
                                                           'research_study_citers_citer_title': 'Integrative genomic analysis of the human immune response to influenza vaccination',
                                                           'research_study_citers_citer_url': 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3713456'}


def test_kf_research_study():
    """Query kf server."""
    with open('tests/fixtures/kf_research_study.json') as fp:
        research_study = json.load(fp)
        assert research_study
        assert isinstance(research_study, dict)
        kf_research_study_summary = ResearchStudySummary(research_study=research_study)
        assert kf_research_study_summary
        extensions = kf_research_study_summary.extensions
        print(extensions)
        assert len(extensions) == 0
        print(kf_research_study_summary.simplified)
        assert kf_research_study_summary.simplified == {'identifier': 'SD_65064P2Z', 'resourceType': 'ResearchStudy',
                                                        'id': '1883519',
                                                        'title': 'INCLUDE: (Sherman) Genomic Analysis of Congenital Heart Defects and Acute Lymphoblastic Leukemia in Children with Down Syndrome',
                                                        'status': 'completed', 'meta': 'SD_65064P2Z',
                                                        'category': '276720006', 'keyword': 'SD65064P2Z'}


def test_gtex_research_study():
    """Query kf server."""
    with open('tests/fixtures/gtex_research_study.json') as fp:
        research_study = json.load(fp)
        # mocker.retrieve = lambda queries: _
        #
        # research_study = mocker.retrieve(['ResearchStudy'])
        assert research_study
        assert isinstance(research_study, dict)
        print(research_study)
        gtex_research_study_summary = ResearchStudySummary(research_study=research_study)
        assert gtex_research_study_summary
        assert gtex_research_study_summary.research_study == research_study
        print(gtex_research_study_summary.research_study)
        extensions = gtex_research_study_summary.extensions
        print(extensions)
        assert len(extensions) == 0
        print(gtex_research_study_summary.simplified)
        assert gtex_research_study_summary.simplified == {'identifier': 'GTEx', 'id': 'f6c7b779-657e-4c89-9a52-d7a39f3c661d', 'resourceType': 'ResearchStudy', 'status': 'completed', 'keyword': 'GTEx', 'meta': 'GTEx'}
