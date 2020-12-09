class Transcripts:
    transcripts=[]
    summaries=[]
    def __init__(self, id_, transcripts, summaries):
        self.id = id_
        self.transcripts.append(transcripts)
        self.summaries.append(summaries)