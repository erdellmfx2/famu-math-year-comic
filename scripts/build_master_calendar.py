#!/usr/bin/env python3
"""Build daily master story calendar by merging academic phases, holidays, syllabus cadence, and FAMU sports schedules."""
import csv, json, re
from datetime import date, timedelta
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from collections import Counter

repo=Path(__file__).resolve().parents[1]
out_dir=repo/'story'
out_dir.mkdir(parents=True,exist_ok=True)

start=date(2025,8,1)
end=date(2026,8,9)

def daterange(a,b):
    d=a
    while d<=b:
        yield d
        d+=timedelta(days=1)

def parse_sidearm_schedule(url,sport,season_type):
    html=requests.get(url,timeout=30,headers={'User-Agent':'Mozilla/5.0'}).text
    soup=BeautifulSoup(html,'html.parser')
    games=[]
    for li in soup.find_all('li',attrs={'data-game-id':True}):
        d_el=li.select_one('.sidearm-schedule-game-opponent-date span') or li.select_one('.sidearm-schedule-game-opponent-date')
        opp_el=li.select_one('.sidearm-schedule-game-opponent-name')
        loc_el=li.select_one('.sidearm-schedule-game-location span') or li.select_one('.sidearm-schedule-game-location')
        if not d_el or not opp_el:
            continue
        d_txt=' '.join(d_el.get_text(' ',strip=True).split())
        m=re.search(r'([A-Za-z]{3,9})\s+(\d{1,2})',d_txt)
        if not m:
            continue
        mon_map={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
        mon=mon_map.get(m.group(1)[:3].title()); day=int(m.group(2))
        if not mon:
            continue
        if season_type=='single_2025':
            yr=2025
        elif season_type=='single_2026':
            yr=2026
        else:
            yr=2025 if mon>=8 else 2026
        try:
            gd=date(yr,mon,day)
        except ValueError:
            continue
        cls=li.get('class') or []
        homeaway='vs'
        if 'sidearm-schedule-away-game' in cls: homeaway='at'
        elif 'sidearm-schedule-neutral-game' in cls: homeaway='vs (neutral)'
        opp=' '.join(opp_el.get_text(' ',strip=True).split())
        loc=' '.join(loc_el.get_text(' ',strip=True).split()) if loc_el else ''
        games.append({'date':gd.isoformat(),'sport':sport,'event':f"{sport}: {homeaway} {opp}",'location':loc,'source':url})
    dedup={(g['date'],g['event']):g for g in games}
    return sorted(dedup.values(), key=lambda x:(x['date'],x['event']))

academic_blocks=[
    ('college_prep', date(2025,8,1), date(2025,8,24)),
    ('fall_classes', date(2025,8,25), date(2025,12,5)),
    ('fall_finals', date(2025,12,6), date(2025,12,12)),
    ('winter_break', date(2025,12,13), date(2026,1,4)),
    ('spring_classes', date(2026,1,5), date(2026,4,24)),
    ('spring_finals', date(2026,4,25), date(2026,5,1)),
    ('summer_break', date(2026,5,2), date(2026,5,10)),
    ('summer_a', date(2026,5,11), date(2026,6,19)),
    ('summer_break', date(2026,6,20), date(2026,6,28)),
    ('summer_b', date(2026,6,29), date(2026,8,7)),
    ('summer_wrap', date(2026,8,8), date(2026,8,9)),
]
def phase_for(d):
    for name,a,b in academic_blocks:
        if a<=d<=b:
            return name
    return 'out_of_range'

holidays={
    '2025-09-01':'Labor Day','2025-11-11':'Veterans Day','2025-11-27':'Thanksgiving Day','2025-11-28':'Thanksgiving Break',
    '2025-12-25':'Christmas Day','2026-01-01':'New Year\'s Day','2026-01-19':'Martin Luther King Jr. Day',
    '2026-05-25':'Memorial Day','2026-06-19':'Juneteenth','2026-07-04':'Independence Day'
}

def syllabus_events_for(d,phase):
    ev=[]; wd=d.weekday()
    if phase in ('fall_classes','spring_classes','summer_a','summer_b'):
        if wd==0: ev.append('Calculus problem set assigned')
        if wd==2: ev.append('Quiz / concept check window')
        if wd==4: ev.append('Office hours + study hall emphasis')
        if wd==6: ev.append('Homework due + weekly planning reset')
    if phase in ('fall_classes','spring_classes') and 6<=d.day<=12 and wd in (1,2,3):
        ev.append('Midterm-style exam window')
    if phase in ('fall_finals','spring_finals'):
        ev.append('Final exams period')
    return ev

sports=[]
for url,sport,stype in [
    ('https://famuathletics.com/sports/football/schedule/2025','Football','single_2025'),
    ('https://famuathletics.com/sports/mens-basketball/schedule/2025-26','Mens Basketball','split_2025_26'),
    ('https://famuathletics.com/sports/baseball/schedule/2026','Baseball','single_2026'),
    ('https://famuathletics.com/sports/softball/schedule/2026','Softball','single_2026'),
]:
    sports.extend(parse_sidearm_schedule(url,sport,stype))
sports_by_date={}
for g in sports:
    sports_by_date.setdefault(g['date'],[]).append(g)

prep_malik=['build budget spreadsheet for semester','compare meal-plan spending and textbook costs','map actuarial pathway milestones','set up class folders and calendar reminders']
prep_nia=['organize color-coded notes system','visit campus organizations fair','create weekly balance plan (study/rest)','draft personal learning goals']
class_malik=['library deep-work block (2 hours)','practice calculus drills with timer','attend office hours for targeted questions','update internship/career checklist']
class_nia=['lead whiteboard study circle','rewrite notes into concept map','help peer with difficult concept','join student org planning meeting']
finals_malik=['final review packet sprint','past-exam error log and corrections','quiet focus session in library']
finals_nia=['group review facilitation','formula/theorem synthesis session','stress-management check-in + recap']
break_malik=['family time + light review','career reflection and resume polishing','rest and reset routines']
break_nia=['creative reset + reading','journal reflections on growth','light preview of next topics']
prof_touchpoints=[
    'Dr. Brooks: show your reasoning clearly','Dr. Delgado: clean setup before solving','Dr. Okafor: visualize the concept first',
    'Dr. Bennett: interpret numbers as evidence','Dr. Price: state assumptions before modeling'
]

rows=[]
for idx,d in enumerate(daterange(start,end)):
    phase=phase_for(d); ds=d.isoformat(); fixed=[]
    if ds in holidays: fixed.append(f"Holiday: {holidays[ds]}")
    if d==date(2025,8,25): fixed.append('Fall semester classes begin (story backbone)')
    if d==date(2026,1,5): fixed.append('Spring semester classes begin (story backbone)')
    if d==date(2026,5,11): fixed.append('Summer A begins (story backbone)')
    if d==date(2026,6,29): fixed.append('Summer B begins (story backbone)')
    if d==date(2026,8,7): fixed.append('Summer term wrap week')

    sy=syllabus_events_for(d,phase)
    sports_events=[g['event'] for g in sports_by_date.get(ds,[])]

    if phase=='college_prep':
        malik=prep_malik[idx%len(prep_malik)]; nia=prep_nia[idx%len(prep_nia)]
    elif phase in ('fall_classes','spring_classes','summer_a','summer_b'):
        malik=class_malik[idx%len(class_malik)]; nia=class_nia[idx%len(class_nia)]
    elif phase in ('fall_finals','spring_finals'):
        malik=finals_malik[idx%len(finals_malik)]; nia=finals_nia[idx%len(finals_nia)]
    else:
        malik=break_malik[idx%len(break_malik)]; nia=break_nia[idx%len(break_nia)]

    priority='normal'
    if sports_events or any('Midterm' in e or 'Final exams' in e for e in sy): priority='high'
    if ('Final exams period' in sy and sports_events) or len(sports_events)>=2: priority='peak'

    hint='campus slice-of-life'
    if sports_events and 'Football' in ' '.join(sports_events): hint='game-day energy + academics balance'
    elif any('Final exams' in e for e in sy): hint='high-pressure study + emotional support'
    elif 'Holiday' in ' '.join(fixed): hint='family/community reflection moment'

    rows.append({
        'date':ds,'academic_phase':phase,'fixed_events':' | '.join(fixed),'syllabus_events':' | '.join(sy),'sports_events':' | '.join(sports_events),
        'character_activity_malik':malik,'character_activity_nia':nia,'professor_touchpoint':prof_touchpoints[idx%len(prof_touchpoints)],
        'comic_scene_hint':hint,'priority_score':priority
    })

csv_path=out_dir/'master_calendar_2025_2026.csv'
fields=list(rows[0].keys())
with open(csv_path,'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
(out_dir/'master_calendar_2025_2026.json').write_text(json.dumps(rows,indent=2))

pc=Counter(r['academic_phase'] for r in rows)
md=['# Master Calendar 2025-2026 (Daily Story Backbone)','',f'Date range: **{start} to {end}**','',f'Total days: **{len(rows)}**','','## Phase counts','']
for k,v in pc.items(): md.append(f'- {k}: {v} days')
md += ['','## High / Peak pressure sample days','']
for r in [x for x in rows if x['priority_score'] in ('high','peak')][:40]:
    md.append(f"- {r['date']} ({r['priority_score']}): {r['sports_events'] or r['syllabus_events'] or r['fixed_events']}")
md += ['', '## Notes', '- Daily activities are narrative-ready prompts for Malik and Nia.', '- Sports pulled from official FAMU athletics schedule pages.', '- Academic blocks use semester backbone assumptions aligned to gathered calendar artifacts.']
(out_dir/'master_calendar_2025_2026.md').write_text('\n'.join(md))

(out_dir/'master_calendar_sources.md').write_text('\n'.join([
'# Master Calendar Sources & Assumptions','',
'## Repo Sources',
'- research/academic-calendars/fall_2025.pdf','- research/academic-calendars/spring_2026.pdf','- research/academic-calendars/summer_2025.pdf',
'- research/course-syllabi/calculus-1/FAMU_MAC2311_Calculus_I_Fall_2023_syllabus.pdf','- research/course-syllabi/calculus-2/*','- research/course-syllabi/calculus-3/*','',
'## Live Sources (Sports)','- https://famuathletics.com/sports/football/schedule/2025','- https://famuathletics.com/sports/mens-basketball/schedule/2025-26','- https://famuathletics.com/sports/baseball/schedule/2026','- https://famuathletics.com/sports/softball/schedule/2026','',
'## Live Source (Events)','- https://www.famu.edu/events/index.php (reference; event detail appears JS-driven)','',
'## Assumptions','- Story year window fixed to 2025-08-01 through 2026-08-09.','- Semester phase boundaries set to create a complete daily narrative backbone when exact per-day registrar dates are not machine-extracted from PDFs in this environment.','- Holiday layer uses major US federal holidays and common campus break periods.','- Syllabus layer modeled as recurring workload cadence (assignments/quizzes/midterm windows/finals periods).',
]))

print('master calendar built:',len(rows),'days')
