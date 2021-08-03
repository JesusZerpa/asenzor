// Transcrypt'ed from Python, 2021-08-02 21:47:03
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import {Vue} from './asenzor.py.vuepy.js';
import {Support} from './asenzor.py.support.js';
import {Plugins} from './asenzor.py.plugins.js';
import {Edit} from './asenzor.py.edit.js';
import {Media} from './asenzor.py.media.js';
import {Table, ToolBar} from './asenzor.py.table.js';
var __name__ = '__main__';
export var element = require ('element-ui');
element.locale ('en');
Vue.use (element);
if (document.querySelector ('#table_app')) {
	window.table = Table ().mount ('#table');
	window.toolbar = ToolBar ().mount ('#toolbar');
}
if (document.querySelector ('#media_modal')) {
	window.media = Media ().mount ('#media_modal');
	// pass;
}
if (document.querySelector ('#edit_app')) {
	window.edit = Edit ().mount ('#edit_app');
}
if (document.querySelector ('#install_plugins')) {
	window.plugins = Plugins ().mount ('#install_plugins');
}
if (document.querySelector ('#support_app')) {
	window.plugins = Support ().mount ('#support');
	window.table = Table ().mount ('#table');
}
export var sticky = function () {
	var altura = $ ('.navbar').offset ().top;
	var py_switch = function () {
		if ($ (window).scrollTop () > altura) {
			$ ('.navbar').addClass ('navbar-fixed');
		}
		else {
			$ ('.navbar').removeClass ('navbar-fixed');
		}
	};
	$ (window).on ('scroll', py_switch);
};
if (location.href == ASENZOR_URL) {
	fetch ('https://zerpatechnology.com.ve/asenzor/json/last-version').then ();
}
$ (document).ready (sticky);

//# sourceMappingURL=asenzor.py.main.map