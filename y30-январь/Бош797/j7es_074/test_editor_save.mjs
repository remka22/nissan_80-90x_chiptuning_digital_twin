// Проверка сохранения редактора: настоящие BIN, запись на диск и обратное чтение.
import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFile, writeFile, mkdtemp, rm, readdir} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join, dirname} from 'node:path';
import {fileURLToPath} from 'node:url';

const root=dirname(fileURLToPath(import.meta.url));
const html=await readFile(join(root,'редактор калибровок j7es ИИ.html'),'utf8');
const script=new vm.Script(html.match(/<script>([\s\S]*?)<\/script>/)[1]);
const source=await readFile(join(root,'j7es_v15.1_весовая-ТОЖ-на-холодную-по-логу-13.38_30.10.26_1440 ИИ.bin'));
const checksumAddresses=new Set([0xFFF8,0xFFF9,0xFFFE,0xFFFF]);

function namedError(name){return Object.assign(new Error(name),{name})}
function element(){return {value:'',textContent:'',innerHTML:'',disabled:false,children:[],style:{},
 appendChild(child){this.children.push(child)},querySelectorAll(){return []}}}
function setup(){
 const elements=new Map(),alerts=[],errors=[];
 const document={getElementById(id){if(!elements.has(id))elements.set(id,element());return elements.get(id)},
  createElement:element,createTextNode:text=>({textContent:text})};
 const context=vm.createContext({document,Uint8Array,atob,console:{error:error=>errors.push(error)},alert:message=>alerts.push(message)});
 context.window=context;script.runInContext(context);
 return {context,elements,alerts,errors,run:code=>vm.runInContext(code,context)};
}
function diskDirectory(path,options={}){
 return {name:'прошивки',async getFileHandle(name,{create=false}={}){
  const pathToFile=join(path,name);
  try{await readFile(pathToFile)}catch(error){if(error.code!=='ENOENT')throw error;
   if(!create)throw namedError('NotFoundError');await writeFile(pathToFile,new Uint8Array())}
  return {async createWritable(){return {
   async write(data){if(options.failWrite?.(name))throw namedError('NotAllowedError');await writeFile(pathToFile,data)},
   async close(){},async abort(){}
  }},async getFile(){return {async arrayBuffer(){const bytes=await readFile(pathToFile);
   if(options.corruptRead?.(name))bytes[0]^=1;
   return bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength)}}}};
 }};
}
async function fixture(t,options={}){
 const path=await mkdtemp(join(tmpdir(),'j7es-save-'));
 t.after(()=>rm(path,{recursive:true,force:true}));
 const app=setup(),directory=diskDirectory(path,options);
 app.context.showDirectoryPicker=async()=>directory;
 return {...app,path,directory};
}
async function open(app,bytes,name='прошивка.BIN'){
 const target={files:[{name,async arrayBuffer(){return bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength)}}],value:'selected'};
 await app.elements.get('file').onchange({target});assert.equal(target.value,'');
}
const save=app=>app.elements.get('save').onclick();
const status=app=>app.elements.get('savestatus').textContent;
async function savedPair(app){
 const names=await readdir(app.path);
 const single=names.find(name=>name.endsWith('64К OpenOLT.bin'));
 const double=names.find(name=>name.endsWith('128К ChipLoader.bin'));
 assert.ok(single);assert.ok(double);
 return {single:await readFile(join(app.path,single)),double:await readFile(join(app.path,double))};
}
function verifyContents(single,double,expected){
 assert.equal(single.length,65536);assert.equal(double.length,131072);
 assert.deepEqual(double.subarray(0,65536),single);assert.deepEqual(double.subarray(65536),single);
 let sum=0;for(const byte of single)sum=(sum+byte)&65535;
 assert.equal(sum,single.readUInt16LE(0xFFFE));
 for(let i=0;i<65536;i++)if(!checksumAddresses.has(i))assert.equal(single[i],expected[i],`Изменён лишний байт ${i.toString(16)}`);
}

for(const copies of [1,2]){
 test(`Из ${copies===1?'64':'128'} КБ: две версии с правками, правильной суммой и неизменным кодом`,async t=>{
  const app=await fixture(t),input=Buffer.concat(Array(copies).fill(source));
  await open(app,input);
  app.run("put(DEFS.find(t=>t.addr===0x5FF4),0,10);put(DEFS.find(t=>t.addr===0x9294),0,0.5);cur[0xE7EF]=12;cur[0x6051]^=1");
  const before=Buffer.from(app.run('cur')),expected=Buffer.from(source);
  expected[0x5FF4]=20;expected[0x9294]=64;expected[0xE7EF]=12;expected[0x6051]^=1;
  await save(app);const {single,double}=await savedPair(app);verifyContents(single,double,expected);
  assert.deepEqual(Buffer.from(app.run('cur')),before);assert.deepEqual(input,Buffer.concat(Array(copies).fill(source)));
  assert.match(status(app),/Сохранены и проверены/);assert.equal(app.alerts.length,0);
  assert.equal(app.elements.get('save').disabled,false);
 });
}

test('Без правок 64 КБ совпадает с исходным BIN побайтно',async t=>{
 const app=await fixture(t);await open(app,source);await save(app);
 const {single,double}=await savedPair(app);verifyContents(single,double,source);assert.deepEqual(single,source);
});

test('Выбор сравниваемого BIN не подменяет сохраняемую прошивку',async t=>{
 const app=await fixture(t);await open(app,source);
 app.run("setComparison(STOCK.slice(),'stock.bin')");await save(app);
 const {single,double}=await savedPair(app);verifyContents(single,double,source);
});

test('Повторное сохранение использует выбранную папку и не перезаписывает файлы',async t=>{
 const app=await fixture(t);let picks=0;app.context.showDirectoryPicker=async()=>{picks++;return app.directory};
 await open(app,source);await save(app);
 const first=await readdir(app.path),contents=await Promise.all(first.map(name=>readFile(join(app.path,name))));
 app.run('cur[0x5FF4]=20');await save(app);
 const names=await readdir(app.path);assert.equal(names.length,4);assert.equal(picks,1);
 assert.ok(names.some(name=>name.includes('(2) 64К')));
 for(let i=0;i<first.length;i++)assert.deepEqual(await readFile(join(app.path,first[i])),contents[i]);
});

test('Занятое имя одного из двух файлов сдвигает имена всей пары',async t=>{
 const app=await fixture(t);await open(app,source);
 const existing='прошивка правка 128К ChipLoader.bin';await writeFile(join(app.path,existing),'existing');
 await save(app);assert.equal(await readFile(join(app.path,existing),'utf8'),'existing');
 const names=await readdir(app.path);assert.ok(names.includes('прошивка правка (2) 64К OpenOLT.bin'));
 assert.ok(names.includes('прошивка правка (2) 128К ChipLoader.bin'));
});

test('Отмена выбора папки не создаёт файлов и снимает блокировку',async t=>{
 const app=await fixture(t);await open(app,source);
 app.context.showDirectoryPicker=async()=>{throw namedError('AbortError')};await save(app);
 assert.deepEqual(await readdir(app.path),[]);assert.equal(app.alerts.length,0);assert.equal(status(app),'');
 assert.equal(app.elements.get('save').disabled,false);
});

test('Ошибки доступа к папке видны пользователю',async t=>{
 const app=await fixture(t);await open(app,source);
 app.context.showDirectoryPicker=async()=>{throw namedError('NotAllowedError')};await save(app);
 assert.equal(app.alerts.length,1);assert.match(status(app),/Не удалось/);assert.equal(app.errors.length,1);
 assert.equal(app.elements.get('save').disabled,false);
});

test('Ошибка второго файла не выдаётся за успешное сохранение пары',async t=>{
 const app=await fixture(t,{failWrite:name=>name.includes('128К')});await open(app,source);await save(app);
 assert.equal(app.alerts.length,1);assert.match(status(app),/Не используйте файлы этой попытки/);
 assert.match(status(app),/64К OpenOLT/);assert.match(status(app),/128К ChipLoader/);
 assert.equal(app.elements.get('save').disabled,false);
});

test('Обратное чтение обнаруживает повреждение и останавливает сохранение',async t=>{
 const app=await fixture(t,{corruptRead:()=>true});await open(app,source);await save(app);
 assert.equal(app.alerts.length,1);assert.match(status(app),/Не удалось сохранить и проверить/);
 assert.equal((await readdir(app.path)).length,1);
});

test('Повторный клик не запускает вторую запись; сохраняется состояние на момент нажатия',async t=>{
 const app=await fixture(t);await open(app,source);let release,picks=0;
 app.context.showDirectoryPicker=()=>{picks++;return new Promise(resolve=>{release=resolve})};
 const pending=save(app);assert.equal(app.elements.get('save').disabled,true);
 app.run('cur[0x5FF4]=20;refresh()');assert.equal(app.elements.get('save').disabled,true);
 await save(app);release(app.directory);await pending;assert.equal(picks,1);
 const {single,double}=await savedPair(app);verifyContents(single,double,source);
});

test('Можно сменить папку; отмена сохраняет прежний выбор',async t=>{
 const app=await fixture(t);await open(app,source);
 await app.elements.get('savefolder').onclick();assert.equal(app.run('saveDirectory.name'),'прошивки');
 app.context.showDirectoryPicker=async()=>{throw namedError('AbortError')};
 await app.elements.get('savefolder').onclick();assert.equal(app.run('saveDirectory.name'),'прошивки');await save(app);
 assert.equal((await readdir(app.path)).length,2);
});

test('Браузер без выбора папки показывает понятное сообщение',async t=>{
 const app=await fixture(t);await open(app,source);delete app.context.showDirectoryPicker;await save(app);
 assert.equal(app.alerts.length,1);assert.match(app.alerts[0],/Google Chrome или Microsoft Edge/);
 assert.deepEqual(await readdir(app.path),[]);assert.equal(app.elements.get('save').disabled,false);
});

test('128 КБ с разными половинами и неверный размер не заменяют открытую прошивку',async t=>{
 const app=await fixture(t);await open(app,source);
 const invalid=Buffer.concat([source,source]);invalid[65536]^=1;await open(app,invalid);
 await open(app,Buffer.alloc(10));assert.equal(app.alerts.length,2);
 assert.deepEqual(Buffer.from(app.run('cur')),source);
});
