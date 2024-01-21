import pandas as pd
import argparse
import datetime
import logging
import intake
import copy
import os

def createDataFrameSummary(df: pd.core.frame.DataFrame
                          ) -> pd.core.frame.DataFrame:             # return summary dataframe
    '''
        Create a simple summary of a dataframe
    '''
    s_df = df.describe(include='all').T[['count','unique','top','freq']]            # use pandas.describe to summarize dataFrame
    s_df['Count %'] = (0.5 + (100 * s_df['count'] / len(df))).astype(int)           # Add Count % column (integer percents) to summary
    return s_df


def showCountsx(report: str,
               field: str):
    cnt_d = {'report':report, 'field':field, 'cnt':data_d[report]['summary'].loc[field,'count'], 'unique':data_d[report]['summary'].loc[field,'unique']}    
    lggr.info(f"{report} Report {field}: {data_d[report]['summary'].loc[field,'count']} unique: {data_d[report]['summary'].loc[field,'unique']}")
    return cnt_d


def findPublicationYear(row):
    '''
        The CHORUS reports include an Online Publication Year and a Print Publication Year.
        In order to include as many connections as possible, we need to combine these two columns.
        They are typically within one of each other, so it is generally a small change in the data.
    '''

    s = None                                                        # initialize s

    if 'Print Publication Date' in row.index:
        first =  'Print Publication Date'
    else:
        first = 'Publication_Print'

    if 'Online Publication Date' in row.index:
        second = 'Online Publication Date'
    else:
        second = 'Publication_Online'

    if isinstance(row[first], str):              # if Print Publication Date is a string
        s = row[first]
    elif isinstance(row[second], str):
        s = row[second]
    else:
        return

    if s:
        try:
            yr = pd.to_datetime(s, errors='coerce').dt.year
        except:
            yr = pd.to_datetime(s.split('T')[0], errors='coerce').year

        return yr

def str2year(s):
    '''
        This function converts dates expressed as strings into dates and retrieves the
        year from the date. str2year wraps the pandas.to_datetime functions as
        pd.to_datetime does this very well for many date formats, but it doesn't seem to
        handle timestamps...
    '''
    if not isinstance(s, str):
        return None
    
    try:
        yr = pd.to_datetime(s, errors='coerce').dt.year
    except:
        yr = pd.to_datetime(s.split('T')[0], errors='coerce').year

    return yr
    

class CHORUSReport:
    def __init__(self, dataPath):
        self.dataPath       = dataPath                                      # argument is the path of the data
        self.dataFile       = self.dataPath.split('/')[-1]                  # get file name from path
        organization, year, month, day, rt   = self.dataFile.split('-')     # get organization and timestamp from the file name

        self.organization   = organization                                  # set object properties
        self.timestamp      = ''.join([year, month, day])
        rt = rt.replace('Report.csv','')
        if rt == 'All':
            self.dataType       = 'all'
        elif rt== 'AuthorAffiliation':
            self.dataType       = 'authors'
        else:
            self.dataType       = 'datasets'

        self.data_d             = {}

        if 'intake:' in dataPath:
            catalogName = CHORUSCatalogDirectory + '/' + 'chorusCatalog.yaml'
            intakeCat = intake.open_catalog(catalogName)
            sourceName    = '-'.join([organization,timestamp[0:4], timestamp[4:6], timestamp[6:8], dataTypes_d[self.dataType]['fileTitle']])
            self.data_d.update({'data':      intakeCat[sourceName].read()}) # add dataframe to dictionary
        else:
            self.data_d.update({'dataFile': dataPath})
            self.data_d.update({'data': pd.read_csv(dataPath, sep=',', encoding='utf-8')}) # add dataframe to dictionary

        self.data_d.update({'recordCount': len(self.data_d['data'])})

        data_df = self.data_d['data']
        self.data_d.update({'summary': createDataFrameSummary(data_df)})            # create summary dataframe
        summary_df = self.data_d['summary']                                         # pick summary dayaframe
        
        cols = ['organization','date','report','Property'] + list(summary_df.columns)     # add summary columns
        summary_df['top']           = summary_df['top'].str[:24]
        summary_df['organization']  = self.organization
        summary_df['date']          = self.timestamp
        summary_df['report']        = self.dataType
        summary_df['Property']      = summary_df.index
        self.data_d['summary']      = summary_df[cols] 
        self.data_d['data'].replace(r'^\s*$', None, regex=True, inplace=True)    # replace empty strings in dataframe with None to avoid counting them

    def x__init__(self, organization, timestamp, reportType):
        self.organization   = organization          # the organization selected for the report (typically funder)
        self.timestamp      = timestamp             # the time of retrieval of the report (YYYYMMDD_HH)
        self.data_d         = {}

    def __str__(self):
        return f"Datatype: {self.dataType} File: {self.dataFile} {self.data_d['recordCount']} rows"

    def data(self):
        return self.data_d['data']

    def summary(self):
        return self.data_d['summary']

    def counts(self,
               field: str):
        cnt_d = {'report':self.dataType, 'field':field, 'total count':self.summary().loc[field,'count'], 'unique':self.summary().loc[field,'unique']}
        return cnt_d


class CHORUSRetrieval:
    def __init__(self, organization, timestamp, dir, dataType_l = ['all', 'authors', 'datasets']):

        self.report_d = {}
        self.organization   = organization                                  # set object properties
        self.timestamp      = timestamp

        for dt in dataType_l:
            fileName        = '-'.join([organization,timestamp[0:4], timestamp[4:6], timestamp[6:8], dataTypes_d[dt]['fileTitle']]) + 'Report.csv'
            dataFile        = dir + '/' + fileName             # data in dataDir/dataType/dataType.csv
            self.report_d.update({dt: CHORUSReport(dataFile)}) # add dataframe to dictionary

    def __str__(self):
        s = f'Organization: {self.organization} Timestamp: {self.timestamp} Reports: {self.report_d.keys()}\n'
        for r in self.report_d.keys():
            s += str(self.report_d[r]) + '\n'
        return s
    
    def dataTypes(self):
        return list(self.report_d.keys())
        
    def data(self, dt):
        return self.report_d[dt].data_d['data']                 # return dataframe for all report
    
    def summary(self, dt):
        return self.report_d[dt].data_d['summary']              # return dataframe for all report

    def all(self):
        return self.report_d['all'].data_d['data']              # return dataframe for all report
    
    def authors(self):
        return self.report_d['authors'].data_d['data']          # return dataframe for authors report
    
    def datasets(self):
        return self.report_d['datasets'].data_d['data']             # return dataframe for all report
    
    def counts(self, dt, field):
        return self.report_d[dt].counts(field)
    
    '''
        DOI Consistency Check
        The All Report has a row for each DOI and we expect them to all be unique, i.e. total count = unique. 
        The All Report also includes Authors and Datasets columns which have ";" separated lists of the authors 
        and datasets associated with each DOI. The all counts for these fields give the **number of DOIs with 
        associated authors and datasets**, not the total number of authors and datasets. These counts are <= to 
        the toal number of DOIs.  
        The Author Report has a row for each author (total count). The unique count is the number of DOIs with authors. 
        If all of the DOIs in the All Report are in the Author Report, the number of unique DOIs in these two reports would be equal.  
        The Dataset Report has datasets that are connected to the articles. These are discovered in ScholeXplorer. 
        The number of DOIs in this report reflects the number of connections discoverable usig ScholeXplorer.
    '''
    def doiConsistency(self):
        '''
            DOI Consistency Check
            The All Report has a row for each DOI and we expect them to all be unique, i.e. total count = unique. 
            The All Report also includes Authors and Datasets columns which have ";" separated lists of the authors 
            and datasets associated with each DOI. The all counts for these fields give the **number of DOIs with 
            associated authors and datasets**, not the total number of authors and datasets. These counts are <= to 
            the toal number of DOIs.  
            The Author Report has a row for each author (total count). The unique count is the number of DOIs with authors. 
            If all of the DOIs in the All Report are in the Author Report, the number of unique DOIs in these two reports would be equal.  
            The Dataset Report has datasets that are connected to the articles. These are discovered in ScholeXplorer. 
            The number of DOIs in this report reflects the number of connections discoverable usig ScholeXplorer.
        '''
        cnt_l = []
        cnt_d = {}
        cnt_d.update(self.counts('all', 'DOI'))
        cnt_l.append(copy.deepcopy(cnt_d))
        cnt_d.update(self.counts('all', 'Author(s)'))
        cnt_l.append(copy.deepcopy(cnt_d))
        cnt_d.update(self.counts('all', 'Datasets'))
        cnt_l.append(copy.deepcopy(cnt_d))
        cnt_d.update(self.counts('authors', 'DOI'))
        cnt_l.append(copy.deepcopy(cnt_d))
        cnt_d.update(self.counts('datasets', 'Article DOI'))
        cnt_l.append(copy.deepcopy(cnt_d))
        cnt_df = pd.DataFrame(cnt_l)
        print(cnt_df)
        doisWithAuthors = round(100 * cnt_df.loc[3,'unique'] / cnt_df.loc[0,'total count'],2)
        print(f"{doisWithAuthors}% of the DOIs in the All report have authors in the Authors report")


class DatasetReport(CHORUSReport):
    dataType    = 'datasets'
    fileTitle   = 'Dataset'
    pass

class AllReport(CHORUSReport):
    dataType = 'all'
    fileTitle   = 'All'
    pass

class AuthorReport(CHORUSReport):
    dataType = 'authors'
    fileTitle = 'AuthorAffiliation'
    pass

CHORUSDataDirectory     = os.getenv("HOME") + '/MetadataGameChanger/ProjectsAndPlans/INFORMATE/CHORUS/data'
CHORUSCatalogDirectory  = os.getenv("HOME") + '/MetadataGameChanger/Repositories/INFORMATE/CHORUS/data'

dataTypes_d = {'all':   {'fileTitle' : 'All',
                         'dtype'    : {'Datasets': 'object',
                                       'Issue': 'object',
                                       'ORCID': 'object',
                                       'Agency Portal URL': 'object',
                                       'Grant ID': 'object'}
                        },
            'authors':  {'fileTitle' : 'AuthorAffiliation',
                         'dtype' :  {'Affiliation': 'object', 
                                     'Issue': 'object',
                                     'ORCID': 'object',
                                     'Volume':'object',
                                     'Agency Portal URL': 'object',
                                     'Datasets (beta)': 'object'}
                        },
            'datasets': {'fileTitle' : 'Dataset',
                         'dtype':{'Award Number': 'object','Award Title': 'object',
                                'Date Dataset Collected at Repository': 'object',
                                'Funder Identifier': 'object',
                                'Funder IdentifierType': 'object',
                                'Funder Name': 'object'}
                        }
}
dataTypes   = list(dataTypes_d)


def main():
    #
    # retrieve command line arguments
    #
    commandLine = argparse.ArgumentParser(prog='CHORUS Reports',
                                          description='Library retrieving and analyzing CHORUS reports'
                                          )
    commandLine.add_argument("-dt","--dataTypes", nargs="*", type=str,    # DOIs on the command line
                        help='space separated list of dataTypes'
                        )
    commandLine.add_argument("-cdd","--CHORUSDataDirectory", type=str,    # DOIs on the command line
                        help='path to CHORUS data'
                        )
    commandLine.add_argument('--compareDOICounts', dest='compareDOICounts', 
                        default=False, action='store_true',
                        help='Compare DOI counts across reports'
                        )    
    commandLine.add_argument('--loglevel', default='info',
                             choices=['debug', 'info', 'warning'],
                             help='Logging level'
                             )
    commandLine.add_argument('--logto', metavar='FILE', nargs="*",
                             help='Log file (will append to file if exists)'
                             )
    # parse the command line and define variables
    args = commandLine.parse_args()

    if args.logto:
        # Log to file
        logging.basicConfig(
            filename=args.logto, filemode='a',
            format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
            level=args.loglevel.upper(),
            datefmt='%Y-%m-%d %H:%M:%S')
    else:
        # Log to stderr
        logging.basicConfig(
            format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
            level=args.loglevel.upper(),
            datefmt='%Y-%m-%d %H:%M:%S')

    lggr = logging.getLogger('DOI Metadata Tools')

    '''
        DOI Consistency Check
        The All Report has a row for each DOI and we expect them to all be unique, i.e. total count = unique. 
        The All Report also includes Authors and Datasets columns which have ";" separated lists of the authors 
        and datasets associated with each DOI. The all counts for these fields give the **number of DOIs with 
        associated authors and datasets**, not the total number of authors and datasets. These counts are <= to 
        the toal number of DOIs.  
        The Author Report has a row for each author (total count). The unique count is the number of DOIs with authors. 
        If all of the DOIs in the All Report are in the Author Report, the number of unique DOIs in these two reports would be equal.  
        The Dataset Report has datasets that are connected to the articles. These are discovered in ScholeXplorer. 
        The number of DOIs in this report reflects the number of connections discoverable usig ScholeXplorer.
    '''
    if args.compareDOICounts is True:
        print(f"{agency} {Date}")
        cnt_l = []
        cnt_d = {'agency':agency, 'date':timestamp}
        cnt_d.update(showCounts('all', 'DOI'))
        cnt_l.append(copy.deepcopy(cnt_d))
        cnt_d.update(showCounts('all', 'Author(s)'))
        cnt_l.append(copy.deepcopy(cnt_d))
        cnt_d.update(showCounts('all', 'Datasets'))
        cnt_l.append(copy.deepcopy(cnt_d))
        cnt_d.update(showCounts('authors', 'DOI'))
        cnt_l.append(copy.deepcopy(cnt_d))
        cnt_d.update(showCounts('datasets', 'Article DOI'))
        cnt_l.append(copy.deepcopy(cnt_d))
        cnt_df = pd.DataFrame(cnt_l)
        print(cnt_df)
        doisWithAuthors = round(100 * cnt_df.loc[3,'unique'] / cnt_df.loc[0,'cnt'],2)
        print(f"{doisWithAuthors}% of the DOIs in the All report have authors in the Authors report")


if __name__ == "__main__":
    main()

