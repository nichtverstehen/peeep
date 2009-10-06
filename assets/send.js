(function() {
var send = function(url, content, type) {
	if (type == null)
		type = 'text/html;charset=utf-8';
	else
		type = type.match(/^[^;]+/)+';charset=utf-8';
		
	var form = document.createElement('form');
	form.setAttribute('method', 'post');
	form.setAttribute('action', 'http://www.peeep.us/upload.php');
	form.setAttribute('enctype', 'multipart/form-data');
	form.setAttribute('accept-charset', 'utf-8');
	var input = document.createElement('input');
	input.setAttribute('type', 'hidden');
	input.setAttribute('name', 'r_content');
	input.setAttribute('value', content);
	form.appendChild(input);
	input = input.cloneNode(false);
	input.setAttribute('name', 'r_url');
	input.setAttribute('value', url);
	form.appendChild(input);
	input = input.cloneNode(false);
	input.setAttribute('name', 'r_type');
	input.setAttribute('value', type);
	form.appendChild(input);
	document.body.appendChild(form);
	form.submit();
	document.body.removeChild(form);
};
var showLoad = function() {
	if (document.getElementById('peeeppeeeppeeep') != null)
		return;
	var div = document.createElement('div'), img = document.createElement('img');
	img.setAttribute('src', 'http://www.peeep.us/assets/load.gif');
	div.appendChild(img);
	div.setAttribute('style', 'position: fixed; left: 50%; top: 0; margin-left: -24px; padding: 8px; background: rgba(255,255,255,0.9);');
	div.id = 'peeeppeeeppeeep';
	document.body.appendChild(div);
};
try {
	showLoad();
	var url = location.href;
	var r = new XMLHttpRequest();
	r.open('GET', url, true);
	//r.overrideMimeType('application/octet-stream');
	r.onreadystatechange = function() {
		try {
			if (r.readyState == 4) {
				if ((r.status >= 200 && r.status < 300) || (r.status >= 400 && r.status < 500)) {
					send(url, r.responseText, r.getResponseHeader('Content-type'));
				} else {
					throw r.statusText;
				}
			}
		}
		catch(e) { alert('Error: '+e+'\nPlease, try again'); }
	};
	r.send(null);
}
catch(e) { alert('Error: '+e+'\nPlease, try again'); }
})();