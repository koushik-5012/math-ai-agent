const BASE = window.location.origin;

async function ask(){
  const status=document.getElementById("status");
  const answerBox=document.getElementById("answer");

  const question=document.getElementById("question").value.trim();
  const image=document.getElementById("image").files[0];
  const audio=document.getElementById("audio").files[0];

  if(!question && !image && !audio){
    status.innerText="❌ Provide text, image or audio";
    return;
  }

  const fd=new FormData();
  if(question) fd.append("question",question);
  if(image) fd.append("image",image);
  if(audio) fd.append("audio",audio);

  status.innerText="⏳ Processing...";
  answerBox.innerText="";

  try{
    const res=await fetch(`${BASE}/ask`,{method:"POST",body:fd});
    const data=await res.json();

    if(!res.ok){
      status.innerText="❌ "+data.detail;
      return;
    }

    status.innerText="✅ Done";
    answerBox.innerText=data.answer;
  }catch(err){
    status.innerText="❌ Backend unreachable";
  }
}

async function sendFeedback(isHelpful){
  await fetch(`${BASE}/feedback`,{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({helpful:isHelpful})
  });
  alert("Thanks for your feedback!");
}