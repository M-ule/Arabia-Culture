from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')


def replace_once(old, new, label):
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 match, found {count}')
    text = text.replace(old, new, 1)


replace_once(
    '"수면까지 남은 시간(h)":"지금부터 취침 전까지 생산 건물을 가동할 시간입니다. 비워 두면 기본 운영 시간을 사용합니다."',
    '"수면까지 남은 시간(h)":"지금부터 취침 전까지 건물을 가동할 시간입니다. 자원 건물도 포함되며, 비워 두면 기본 운영 시간을 사용합니다."',
    'sleep guidance',
)

replace_once(
    '<th data-help="현재 보유 중인 디르함입니다." data-label="현재 보유량">현재 보유량</th><th>운영 시간(h)</th><th>시간당 생산량</th></tr></thead><tbody><tr><td data-label="현재 보유량"><input aria-label="디르함 현재 보유량" id="dirhamStock" step="any" type="number"/></td><td data-label="운영 시간(h)"><input aria-label="디르함 운영 시간" id="dirhamHours" placeholder="기본" step="any" type="number"/></td><td data-label="시간당 생산량"><input aria-label="디르함 시간당 생산량" id="dirhamRate" min="0" step="any" type="number"/></td>',
    '<th data-help="현재 보유 중인 디르함입니다." data-label="현재 보유량">현재 보유량</th><th>시간당 생산량</th><th>운영 시간(h)</th></tr></thead><tbody><tr><td data-label="현재 보유량"><input aria-label="디르함 현재 보유량" id="dirhamStock" step="any" type="number"/></td><td data-label="시간당 생산량"><input aria-label="디르함 시간당 생산량" id="dirhamRate" min="0" step="any" type="number"/></td><td data-label="운영 시간(h)"><input aria-label="디르함 운영 시간" id="dirhamHours" placeholder="기본" step="any" type="number"/></td>',
    'dirham column order',
)

replace_once(
    '<div class="card" id="cityCompositionCard"><div class="sectionbar"><h2>주택·건물 구성</h2><button class="push" id="cityView">상세 보기</button></div><h3>주택</h3><div class="wrap" id="homes"></div><div hidden="" id="cityDetails"><h3 data-tip-key="건물 구성">건물 구성</h3><div class="wrap" id="cityBuildings"></div></div></div>',
    '<div class="card" id="cityCompositionCard"><div class="sectionbar"><h2>주택·건물 구성</h2><button class="push" id="cityView">상세 보기</button></div><div hidden="" id="cityHallDetails"><h3 data-tip-key="건물 구성">건물 구성</h3><div class="wrap" id="cityHallBuildings"></div></div><h3>주택</h3><div class="wrap" id="homes"></div><div hidden="" id="cityDetails"><div class="wrap" id="cityBuildings"></div></div></div>',
    'city composition structure',
)

old_city_rows = ''' $('homes').innerHTML=makeTable(['주택','건물 수','일꾼/채'],Object.entries(c.homes).map(([id,h])=>{const b=CITY_DATA.buildings.find(b=>b.id===id);return '<tr>'+cell(b.name)+cell(ci(h.count,'min="0" data-home="'+id+'" data-field="count"'),'input-cell')+cell(b.levels[h.lv].supply,'calc')+'</tr>';}));
 $('cityBuildings').innerHTML=makeTable(['건물','건물 수','가로×세로','면적 합계','필요 일꾼'],CITY_DATA.buildings.filter(b=>!c.homes[b.id]).map(b=>'<tr>'+cell(b.name)+cell(b.id==='City_CityHall'?'1':ci(c.manual[b.id]??'','min="0" placeholder="기본 '+cityCount({...b})+'" data-building="'+b.id+'"'),'input-cell')+cell(b.w+'×'+b.l,'calc')+cell(fmtQty(cityCount(b)*b.w*b.l),'calc')+cell(fmtQty(cityCount(b)*b.levels[1].workers),'calc')+'</tr>'));'''
new_city_rows = ''' const homeOrder=['Home_Medium','Home_Premium'];
 $('homes').innerHTML=makeTable(['주택','건물 수','일꾼/채'],homeOrder.map(id=>{const h=c.homes[id],b=CITY_DATA.buildings.find(b=>b.id===id);return '<tr>'+cell(b.name)+cell(ci(h.count,'min="0" data-home="'+id+'" data-field="count"'),'input-cell')+cell(b.levels[h.lv].supply,'calc')+'</tr>';}));
 const buildingRow=b=>'<tr>'+cell(b.name)+cell(b.id==='City_CityHall'?'1':ci(c.manual[b.id]??'','min="0" placeholder="기본 '+cityCount({...b})+'" data-building="'+b.id+'"'),'input-cell')+cell(b.w+'×'+b.l,'calc')+cell(fmtQty(cityCount(b)*b.w*b.l),'calc')+cell(fmtQty(cityCount(b)*b.levels[1].workers),'calc')+'</tr>';
 const cityHall=CITY_DATA.buildings.find(b=>b.id==='City_CityHall');
 $('cityHallBuildings').innerHTML=makeTable(['건물','건물 수','가로×세로','면적 합계','필요 일꾼'],cityHall?[buildingRow(cityHall)]:[]);
 const cityBuildingOrder=['Merchant_Average','CamelFarm_Average','Merchant_Premium','Workshop_Coffee','Workshop_Incense','Workshop_OilLamp','Workshop_Carpet','Workshop_Premium','Irrigation_Small','Irrigation_Oasis','Irrigation_Medium','Irrigation_Noria'];
 const cityBuildingById=new Map(CITY_DATA.buildings.map(b=>[b.id,b]));
 const orderedCityBuildings=[...cityBuildingOrder.map(id=>cityBuildingById.get(id)).filter(Boolean),...CITY_DATA.buildings.filter(b=>!c.homes[b.id]&&b.id!=='City_CityHall'&&!cityBuildingOrder.includes(b.id))];
 $('cityBuildings').innerHTML=makeTable(['건물','건물 수','가로×세로','면적 합계','필요 일꾼'],orderedCityBuildings.map(buildingRow));'''
replace_once(old_city_rows, new_city_rows, 'city building render order')

replace_once(
    "$('cityDetails').hidden=!app.views.city;",
    "$('cityHallDetails').hidden=!app.views.city;$('cityDetails').hidden=!app.views.city;",
    'city detail visibility',
)

replace_once(
    "for(const id of ['homes','cityBuildings','construction','dirhamCard'])labelInputs(id);",
    "for(const id of ['homes','cityHallBuildings','cityBuildings','construction','dirhamCard'])labelInputs(id);",
    'city mobile labels',
)

selector_pairs = [
    ('#homes table,#cityBuildings table', '#homes table,#cityHallBuildings table,#cityBuildings table'),
    ('#homes thead,#cityBuildings thead', '#homes thead,#cityHallBuildings thead,#cityBuildings thead'),
    ('#homes tbody,#cityBuildings tbody', '#homes tbody,#cityHallBuildings tbody,#cityBuildings tbody'),
    ('#homes tbody tr,#cityBuildings tbody tr', '#homes tbody tr,#cityHallBuildings tbody tr,#cityBuildings tbody tr'),
    ('#homes tbody td,#cityBuildings tbody td', '#homes tbody td,#cityHallBuildings tbody td,#cityBuildings tbody td'),
    ('#homes tbody td:first-child,#cityBuildings tbody td:first-child', '#homes tbody td:first-child,#cityHallBuildings tbody td:first-child,#cityBuildings tbody td:first-child'),
    ('#homes tbody td:not(:first-child)::before,#cityBuildings tbody td:not(:first-child)::before', '#homes tbody td:not(:first-child)::before,#cityHallBuildings tbody td:not(:first-child)::before,#cityBuildings tbody td:not(:first-child)::before'),
    ('#homes td:first-child>.mobilelabel,#cityBuildings td:first-child>.mobilelabel', '#homes td:first-child>.mobilelabel,#cityHallBuildings td:first-child>.mobilelabel,#cityBuildings td:first-child>.mobilelabel'),
]
for old, new in selector_pairs:
    if old not in text:
        raise SystemExit(f'mobile selector missing: {old}')
    text = text.replace(old, new)

path.write_text(text, encoding='utf-8')
