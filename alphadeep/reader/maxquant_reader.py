# AUTOGENERATED! DO NOT EDIT! File to edit: nbdev_nbs/reader/maxquant_reader.ipynb (unless otherwise specified).

__all__ = ['parse_modseq', 'MaxQuantReader', 'MaxQuantMSMSReader']

# Cell
import pandas as pd
import numba
import numpy as np

from alphadeep.reader.psm_reader import PSMReaderBase, \
    psm_reader_provider, PSMReader_w_FragBase,\
    psm_w_frag_reader_provider

from alphabase.peptide.fragment import \
    init_fragment_by_precursor_dataframe

@numba.njit
def parse_modseq(
    modseq,
    mod_sep='()',
    fixed_C=True,
    underscore_for_ncterm=True,
):
    PeptideModSeq = modseq
    mod_list = []
    site_list = []
    site = PeptideModSeq.find(mod_sep[0])
    while site != -1:
        site_end = PeptideModSeq.find(mod_sep[1],site+1)+1
        if site_end < len(PeptideModSeq) and PeptideModSeq[site_end] == mod_sep[1]:
            site_end += 1
        if underscore_for_ncterm: site_list.append(str(site-1))
        else: site_list.append(str(site))
        mod_list.append(PeptideModSeq[site-1:site_end])
        PeptideModSeq = PeptideModSeq[:site] + PeptideModSeq[site_end:]
        site = PeptideModSeq.find(mod_sep[0], site)
    if fixed_C:
        site = PeptideModSeq.find('C')
        while site != -1:
            if underscore_for_ncterm: site_list.append(str(site))
            else: site_list.append(str(site+1))
            mod_list.append(f'C{"Carbamidomethyl (C)".join(mod_sep)}')
            site = PeptideModSeq.find('C',site+1)
    return ';'.join(mod_list), ';'.join(site_list)


class MaxQuantReader(PSMReaderBase):
    def __init__(self):
        super().__init__()

        self.mod_sep = '()'
        self.underscore_for_ncterm=True
        self.fixed_C = True

        self.modification_convert_dict = {}
        self.modification_convert_dict['_(Acetyl (Protein N-term))'] = 'Acetyl@Protein N-term'
        self.modification_convert_dict['C(Carbamidomethyl (C))'] = 'Carbamidomethyl@C'
        self.modification_convert_dict['M(Oxidation (M))'] = 'Oxidation@M'
        self.modification_convert_dict['S(Phospho (S))'] = 'Phospho@S'
        self.modification_convert_dict['T(Phospho (T))'] = 'Phospho@T'
        self.modification_convert_dict['Y(Phospho (Y))'] = 'Phospho@Y'
        self.modification_convert_dict['S(Phospho (ST))'] = 'Phospho@S'
        self.modification_convert_dict['T(Phospho (ST))'] = 'Phospho@T'
        self.modification_convert_dict['S(Phospho (STY))'] = 'Phospho@S'
        self.modification_convert_dict['T(Phospho (STY))'] = 'Phospho@T'
        self.modification_convert_dict['Y(Phospho (STY))'] = 'Phospho@Y'
        self.modification_convert_dict['N(Deamidation (NQ))'] = 'Deamidated@N'
        self.modification_convert_dict['Q(Deamidation (NQ))'] = 'Deamidated@Q'
        self.modification_convert_dict['K(GlyGly (K))'] = 'GlyGly@K'
        self.modification_convert_dict['_(ac)'] = 'Acetyl@Protein N-term'
        self.modification_convert_dict['M(ox)'] = 'Oxidation@M'
        self.modification_convert_dict['S(ph)'] = 'Phospho@S'
        self.modification_convert_dict['T(ph)'] = 'Phospho@T'
        self.modification_convert_dict['Y(ph)'] = 'Phospho@Y'
        self.modification_convert_dict['K(gl)'] = 'GlyGly@K'
        self.modification_convert_dict['E(Glu->pyro-Glu)'] = 'Glu->pyro-Glu@E^Protein N-term'
        self.modification_convert_dict['C(UniMod:4)'] = 'Carbamidomethyl@C'
        self.modification_convert_dict['M(UniMod:35)'] = 'Oxidation@M'
        self.modification_convert_dict['S(UniMod:21)'] = 'Phospho@S'
        self.modification_convert_dict['T(UniMod:21)'] = 'Phospho@T'
        self.modification_convert_dict['Y(UniMod:21)'] = 'Phospho@Y'

        for key, val in list(self.modification_convert_dict.items()):
            self.modification_convert_dict[f'{key[0]}[{key[2:-1]}]'] = val

        self.column_mapping = {
            'sequence': 'Sequence',
            'charge': 'Charge',
            'RT': 'Retention time',
            'norm_RT': 'RT',
            'CCS': 'CCS',
            'mobility': ['Mobility','IonMobility'],
            'spec_idx': ['Scan number','MS/MS scan number'],
            'raw_name': 'Raw file',
            'score': 'Score',
            'proteins': 'Proteins',
            'genes': ['Gene Names','Gene names'],
            'decoy': 'decoy',
        }
        self.modseq_col = 'Modified sequence'

    def _load_file(self, filename):
        df = pd.read_csv(filename, sep='\t')
        if not self.keep_all_psm:
            df = df[(df['Reverse']!='+')&(~pd.isna(df['Retention time']))]
        df.reset_index(drop=True,inplace=True)
        df.fillna('', inplace=True)
        min_rt = df['Retention time'].min()
        df['norm_RT'] = (
            df['Retention time']-min_rt
        )/(df['Retention time'].max()-min_rt)
        df['decoy'] = 0
        df.loc[df['Reverse']=='+','decoy'] == 1
        return df

    def _translate_columns(self, origin_df: pd.DataFrame):
        super()._translate_columns(origin_df)
        (
            self._psm_df['mods'],
            self._psm_df['mod_sites']
        ) = zip(
            *origin_df[self.modseq_col].apply(
                parse_modseq, mod_sep=self.mod_sep,
                fixed_C=self.fixed_C,
                underscore_for_ncterm=self.underscore_for_ncterm
            )
        )

class MaxQuantMSMSReader(MaxQuantReader, PSMReader_w_FragBase):
    def __init__(self,
        frag_types=['b','y','b-modloss','y-modloss'],
        max_frag_charge=2,
        frag_tol=20, frag_ppm=True,
    ):
        PSMReader_w_FragBase.__init__(self,
            frag_types = frag_types,
            max_frag_charge = max_frag_charge,
            frag_tol = frag_tol, frag_ppm=frag_ppm
        )

        MaxQuantReader.__init__(self)
        self.keep_all_psm = False
        self._score_thres = 50

    @property
    def fragment_inten_df(self):
        return self._fragment_inten_df

    def _load_file(self, filename):
        df = super()._load_file(filename)
        df = df[df.Score >= self._score_thres]
        df.reset_index(drop=True, inplace=True)
        return df

    def _post_process(self,
        filename, mq_df
    ):
        MaxQuantReader._post_process(self, filename, mq_df)

        self._fragment_inten_df = init_fragment_by_precursor_dataframe(
            mq_df, self.charged_frag_types
        )

        frag_col_dict = dict(zip(
            self.charged_frag_types,
            range(len(self.charged_frag_types))
        ))

        for ith_psm, (nAA, start,end) in enumerate(
            mq_df[['nAA','frag_start_idx','frag_end_idx']].values
        ):
            intens = np.zeros((nAA-1, len(self.charged_frag_types)))

            frag_types = mq_df.loc[ith_psm,'Matches'].split(';')
            if len(frag_types) < 5: continue
            frag_intens = mq_df.loc[ith_psm,'Intensities']
            for frag_type, frag_inten in zip(
                frag_types, frag_intens.split(';')
            ):
                if '-' in frag_type: continue
                idx = frag_type.find('(')
                charge = '1'
                if idx > 0:
                    frag_type, charge = frag_type[:idx], frag_type[idx+1:-2]
                frag_type, frag_pos = frag_type[0], int(frag_type[1:])
                if frag_type in 'xyz':
                    frag_pos = nAA - frag_pos -1
                else:
                    frag_pos -= 1
                frag_type += '_'+charge
                if frag_type not in frag_col_dict: continue
                frag_col = frag_col_dict[frag_type]

                intens[frag_pos,frag_col] = float(frag_inten)

            if np.any(intens==0):
                intens /= np.max(intens)
            self._fragment_inten_df.iloc[
                start:end,:
            ] = intens


        self._psm_df[
            ['frag_start_idx','frag_end_idx']
        ] = mq_df[['frag_start_idx','frag_end_idx']]

    def load_fragment_inten_df(self,
        psm_df, ms_files=None
    ):
        raise NotImplementedError(
            f'"{self.__class__}" must implement "load_fragment_inten_df()"'
        )


psm_reader_provider.register_reader('maxquant', MaxQuantReader)
psm_w_frag_reader_provider.register_reader('maxquant', MaxQuantMSMSReader)