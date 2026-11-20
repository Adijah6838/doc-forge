import { useState } from "react";
export default function App(){
  const [code,setCode]=useState("def add(a, b):\n    \"\"\"Add two numbers.\"\"\"\n    return a+b");
  const [result,setResult]=useState(null);
  const [markdown,setMarkdown]=useState("");
  async function analyze(){
    const res=await fetch("http://127.0.0.1:8001/api/parse",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({code,filename:"main.py"})});
    const data=await res.json(); setResult(data);
    const exp=await fetch("http://127.0.0.1:8001/api/export",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({code,filename:"main.py"})});
    const ed=await exp.json(); setMarkdown(ed.markdown);
  }
  return (<div style={{maxWidth:900,margin:"20px auto",fontFamily:"sans-serif",padding:20}}>
    <h1>DocForge - Documentation Generator</h1>
    <textarea value={code} onChange={e=>setCode(e.target.value)} rows={10} style={{width:"100%"}} />
    <br/><button onClick={analyze} style={{padding:"10px 20px",marginTop:10}}>Generate Documentation</button>
    {result && (<div><h2>Quality Score: {result.score}%</h2><h3>Functions: {result.functions?.length} | Classes: {result.classes?.length} | Missing: {result.missing?.length}</h3>
    <h3>Missing Documentation</h3><ul>{result.missing?.map((m,i)=><li key={i}>{m.type}: {m.name} (line {m.line})</li>)}</ul></div>)}
    {markdown && (<><h2>Markdown Export</h2><pre style={{background:"#f5f5f5",padding:15,whiteSpace:"pre-wrap"}}>{markdown}</pre></>)}
  </div>);
}
