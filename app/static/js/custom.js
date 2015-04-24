function starrer(fid, rno){
    if(document.getElementById("starclass"+fid).className !="fa fa-star fa-2x")     {
	console.log(String(fid));
	request = $.ajax({
	    url: ".",
	    type: "post",
	    data: {
		star: "1",
		file_id: String(fid),
		user_rno: rno,
	    }
	});
	request.done(function (response, textStatus, jqXHR){
	    console.log(response);
	    document.getElementById("starclass"+fid).className="fa fa-star fa-2x";
	    down_count = parseInt(document.getElementsByName("count"+fid)[0].innerHTML)+1;
	    document.getElementsByName("count"+fid)[0].innerHTML = down_count;

	});
    }
}

