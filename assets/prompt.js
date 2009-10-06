function attachEventImpl(node, evt, fun) {
	if (node.addEventListener !== undefined) {
		node.addEventListener(evt, fun, false);
	} else if (node.attachEvent !== undefined) {
		node.attachEvent('on'+evt, fun);
	}
}
function detachEventImpl(node, evt, fun) {
	if (node.removeEventListener !== undefined) {
		node.removeEventListener(evt, fun, false);
	} else if (node.detachEvent !== undefined) {
		node.detachEvent('on'+evt, fun);
	}
}
if (Array.indexOf === undefined) {
	Array.prototype.indexOf = function (needle) {
		for (var i in this) {
			if (this[i] == needle) {
				return i;
			}
		}
		return -1;
	}
}
function Prompt(input, prompt, defaultValue) {
	if (defaultValue === undefined) {
		defaultValue = '';
	}
	
	this.prompt = prompt;
	this.defaultValue = defaultValue;
	this.input = input;
	input.prompt = this;
	
	var _t = this;
	this.focusHandler = function(evt) { _t.displayInput(); };
	this.blurHandler = function(evt) { _t.displayPrompt(); };
	this.submitHandler = function(evt) { _t.displayInput(); };
	this.subclassInput();
	
	this.displayPrompt();
}
Prompt.prototype.displayPrompt = function() {
	if (this.input.value == this.defaultValue) {
		this.input.className += ' prompt';
		this.input.value = this.prompt;
	}
}
Prompt.prototype.displayInput = function() {
	if (this.input.className.split(' ').indexOf('prompt') >= 0) {
		this.input.value = this.defaultValue;
		this.input.className = this.input.className.replace('prompt', '');
	}
}
Prompt.prototype.subclassInput = function() {
	this.unsubclassInput();
	attachEventImpl(input, 'focus', this.focusHandler);
	attachEventImpl(input, 'blur', this.blurHandler);
	if (input.form) 
		attachEventImpl(input.form, 'submit', this.submitHandler);
}
Prompt.prototype.unsubclassInput = function() {
	detachEventImpl(input, 'focus', this.focusHandler);
	detachEventImpl(input, 'blur', this.blurHandler);
	if (input.form) 
		detachEventImpl(input.form, 'submit', this.submitHandler);
}