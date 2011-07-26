var counter=-1;
function newField() {
 	counter++;
	var newFields = document.getElementById('readroot').cloneNode(true);
      	newFields.id = "formcheck"+counter;
        newFields.name= "formcheck"+counter;
	newFields.style.display = 'block';
        document.getElementById('counter').value=counter;
	var newField = newFields.childNodes;
        for (var i=0;i<newField.length;i++) {
		var theName = newField[i].name
		if (theName)
			newField[i].name = theName + counter;
	}
	var insertHere = document.getElementById('writeroot');
	insertHere.parentNode.insertBefore(newFields,insertHere);
}
function unField(){
     counter--;
     document.getElementById('counter').value=counter;
}
