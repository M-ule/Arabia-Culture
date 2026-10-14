from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

def once(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, found {n}')
    s = s.replace(old, new, 1)

once(
    '"수면까지 남은 시간(h)":"지금부터 취침 전까지 건물을 가동할 시간입니다. 자원 건물도 포함되며, 비워 두면 기본 운영 시간을 사용합니다."',
    '"수면까지 남은 시간(h)":"지금부터 취침 전까지 건물을 가동할 시간입니다. 비워 두면 기본 운영 시간을 사용합니다."',
    'sleep tooltip',
)

once(
    '<div class="card" id="cityCompositionCard"><div class="sectionbar"><h2>주택·건물 구성</h2><button class="push" id="cityView">상세 보기</button></div><div hidden="" id="cityHallDetails"><h3 data-tip-key="건물 구성">건물 구성</h3><div class="wrap" id="cityHallBuildings"></div></div><h3>주택</h3><div class="wrap" id="homes"></div><div hidden="" id="cityDetails"><div class="wrap" id="cityBuildings"></div></div></div>',
    '<div class="card" id="cityCompositionCard"><div class="sectionbar"><h2 data-tip-key="건물 구성">건물 구성</h2><button class="push" id="cityView">상세 보기</button></div><div class="wrap" id="cityBuildings"></div></div>',
    'city composition html',
)

old = ''' const homeOrder=['Home_Medium','Home_Premium'];
 $('homes').innerHTML=makeTable(['주택','건물 수','일꾼/채'],homeOrder.map(id=>{const h=c.homes[id],b=CITY_DATA.buildings.find(b=>b.id===id);return '<tr>'+cell(b.name)+cell(ci(h.count,'min="0" data-home="'+id+'" data-field="count"'),'input-cell')+cell(b.levels[h.lv].supply,'calc')+'</tr>';}));
 const buildingRow=b=>'<tr>'+cell(b.name)+cell(b.id==='City_CityHall'?'1':ci(c.manual[b.id]??'','min="0" placeholder="기본 '+cityCount({...b})+'" data-building="'+b.id+'"'),'input-cell')+cell(b.w+'×'+b.l,'calc')+cell(fmtQty(cityCount(b)*b.w*b.l),'calc')+cell(fmtQty(cityCount(b)*b.levels[1].workers),'calc')+'</tr>';
 const cityHall=CITY_DATA.buildings.find(b=>b.id==='City_CityHall');
 $('cityHallBuildings').innerHTML=makeTable(['건물','건물 수','가로×세로','면적 합계','필요 일꾼'],cityHall?[buildingRow(cityHall)]:[]);
 const cityBuildingOrder=['Merchant_Average','CamelFarm_Average','Merchant_Premium','Workshop_Coffee','Workshop_Incense','Workshop_OilLamp','Workshop_Carpet','Workshop_Premium','Irrigation_Small','Irrigation_Oasis','Irrigation_Medium','Irrigation_Noria'];
 const cityBuildingById=new Map(CITY_DATA.buildings.map(b=>[b.id,b]));
 const orderedCityBuildings=[...cityBuildingOrder.map(id=>cityBuildingById.get(id)).filter(Boolean),...CITY_DATA.buildings.filter(b=>!c.homes[b.id]&&b.id!=='City_CityHall'&&!cityBuildingOrder.includes(b.id))];
 $('cityBuildings').innerHTML=makeTable(['건물','건물 수','가로×세로','면적 합계','필요 일꾼'],orderedCityBuildings.map(buildingRow));'''
new = ''' const homeOrder=['Home_Medium','Home_Premium'];
 const homeRow=id=>{const h=c.homes[id],b=CITY_DATA.buildings.find(b=>b.id===id),n=num(h.count),supplyPer=b.levels[h.lv].supply;return '<tr>'+cell(b.name)+cell(ci(h.count,'min="0" data-home="'+id+'" data-field="count"'),'input-cell')+cell(b.w+'×'+b.l,'calc')+cell(fmtQty(n*b.w*b.l),'calc')+cell('확보 '+fmtQty(n*supplyPer)+' ('+fmtQty(supplyPer)+'/채)','calc')+'</tr>';};
 const buildingRow=b=>'<tr data-city-detail="1">'+cell(b.name)+cell(b.id==='City_CityHall'?'1':ci(c.manual[b.id]??'','min="0" placeholder="기본 '+cityCount({...b})+'" data-building="'+b.id+'"'),'input-cell')+cell(b.w+'×'+b.l,'calc')+cell(fmtQty(cityCount(b)*b.w*b.l),'calc')+cell('필요 '+fmtQty(cityCount(b)*b.levels[1].workers),'calc')+'</tr>';
 const cityHall=CITY_DATA.buildings.find(b=>b.id==='City_CityHall');
 const cityBuildingOrder=['Merchant_Average','CamelFarm_Average','Merchant_Premium','Workshop_Coffee','Workshop_Incense','Workshop_OilLamp','Workshop_Carpet','Workshop_Premium','Irrigation_Small','Irrigation_Oasis','Irrigation_Medium','Irrigation_Noria'];
 const cityBuildingById=new Map(CITY_DATA.buildings.map(b=>[b.id,b]));
 const orderedCityBuildings=[...cityBuildingOrder.map(id=>cityBuildingById.get(id)).filter(Boolean),...CITY_DATA.buildings.filter(b=>!c.homes[b.id]&&b.id!=='City_CityHall'&&!cityBuildingOrder.includes(b.id))];
 const cityRows=[...(cityHall?[buildingRow(cityHall)]:[]),...homeOrder.map(homeRow),...orderedCityBuildings.map(buildingRow)];
 $('cityBuildings').innerHTML=makeTable(['건물','건물 수','가로×세로','면적 합계','일꾼'],cityRows);'''
once(old, new, 'city render')

once(
    "function updateNativeViews(){app.views??={prod:false,wonder:false,city:false};for(const id of ['prod','wonder']){$('panel-'+id).classList.toggle('expanded',app.views[id]);$(id+'View').textContent=app.views[id]?'상세 숨기기':'상세 보기';$(id+'View').setAttribute('aria-expanded',String(app.views[id]));}$('cityHallDetails').hidden=!app.views.city;$('cityDetails').hidden=!app.views.city;$('cityView').textContent=app.views.city?'상세 숨기기':'상세 보기';for(const id of ['goalTable','sleepTable','powerTable'])$(id).querySelectorAll('th').forEach((th,j)=>th.classList.toggle('detailcol',j>(id==='goalTable'?2:1)));}",
    "function updateNativeViews(){app.views??={prod:false,wonder:false,city:false};for(const id of ['prod','wonder']){$('panel-'+id).classList.toggle('expanded',app.views[id]);$(id+'View').textContent=app.views[id]?'상세 숨기기':'상세 보기';$(id+'View').setAttribute('aria-expanded',String(app.views[id]));}$('cityBuildings').querySelectorAll('[data-city-detail]').forEach(row=>row.hidden=!app.views.city);$('cityView').textContent=app.views.city?'상세 숨기기':'상세 보기';$('cityView').setAttribute('aria-expanded',String(app.views.city));for(const id of ['goalTable','sleepTable','powerTable'])$(id).querySelectorAll('th').forEach((th,j)=>th.classList.toggle('detailcol',j>(id==='goalTable'?2:1)));}",
    'city view toggle',
)

once(
    "function cityNativeDecorations(){for(const id of ['homes','cityHallBuildings','cityBuildings','construction','dirhamCard'])labelInputs(id);",
    "function cityNativeDecorations(){for(const id of ['cityBuildings','construction','dirhamCard'])labelInputs(id);",
    'city decorations',
)

p.write_text(s, encoding='utf-8')
