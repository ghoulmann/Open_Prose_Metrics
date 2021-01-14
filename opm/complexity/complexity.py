from readability.readability import Readability

def get_scores(text):
    analysis = Readability(text)
    results = {}
    results['ari'] = analysis.ARI()
    results['fkgl'] = analysis.FleschKincaidGradeLevel()
    results['cli'] = analysis.ColemanLiauIndex()
    results['fre'] = analysis.FleschReadingEase()
    results['gfi'] = analysis.GunningFogIndex()
    results['lix'] = analysis.LIX()
    results['rix'] = analysis.RIX()
    results['smog'] = analysis.SMOGIndex()
    return results




