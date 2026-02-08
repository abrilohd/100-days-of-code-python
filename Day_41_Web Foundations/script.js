// Lightweight index script: shows a small console hint and demonstrates a JSON fetch example path
document.addEventListener('DOMContentLoaded',()=>{
  console.log('Day 41 index loaded — open any example from the list.');
  // small demonstration: try to fetch a known JSON if it exists
  const jsonPath = 'KnowJSON/data.json';
  fetch(jsonPath).then(r=>{
    if(!r.ok) throw new Error('no json');
    return r.json();
  }).then(data=>{
    console.log('Loaded KnowJSON/data.json sample:', data);
  }).catch(()=>{
    // silent: file may not exist in every copy
  });
});
