//#region node_modules/@googlemaps/js-api-loader/dist/index.js
function setScriptSrc(script, src) {
	script.src = src;
}
var bootstrap = (bootstrapParams) => {
	var bootstrapPromise;
	var script;
	var bootstrapParamsKey;
	var PRODUCT_NAME = "The Google Maps JavaScript API";
	var GOOGLE = "google";
	var IMPORT_API_NAME = "importLibrary";
	var PENDING_BOOTSTRAP_KEY = "__ib__";
	var doc = document;
	var global_ = window;
	var google_ = global_[GOOGLE] || (global_[GOOGLE] = {});
	var namespace = google_.maps || (google_.maps = {});
	var libraries = /* @__PURE__ */ new Set();
	var searchParams = new URLSearchParams();
	var triggerBootstrap = () => bootstrapPromise || (bootstrapPromise = new Promise(async (resolve, reject) => {
		await (script = doc.createElement("script"));
		searchParams.set("libraries", [...libraries] + "");
		for (bootstrapParamsKey in bootstrapParams) searchParams.set(bootstrapParamsKey.replace(/[A-Z]/g, (g) => "_" + g[0].toLowerCase()), bootstrapParams[bootstrapParamsKey]);
		searchParams.set("callback", GOOGLE + ".maps." + PENDING_BOOTSTRAP_KEY);
		setScriptSrc(script, "https://maps.googleapis.com/maps/api/js?" + searchParams);
		namespace[PENDING_BOOTSTRAP_KEY] = resolve;
		script.onerror = () => bootstrapPromise = reject(Error(PRODUCT_NAME + " could not load."));
		script.nonce = doc.querySelector("script[nonce]")?.nonce || "";
		doc.head.append(script);
	}));
	namespace[IMPORT_API_NAME] ? console.warn(PRODUCT_NAME + " only loads once. Ignoring:", bootstrapParams) : namespace[IMPORT_API_NAME] = (libraryName, ...args) => libraries.add(libraryName) && triggerBootstrap().then(() => namespace[IMPORT_API_NAME](libraryName, ...args));
};
var MSG_DEPRECATED_LOADER = "The Loader class is no longer available in this version.\nPlease use the new functional API: setOptions() and importLibrary().\nFor more information, see the updated documentation at: https://github.com/googlemaps/js-api-loader/blob/main/README.md";
var MSG_REPEATED_SET_OPTIONS = (options) => `The setOptions() function should only be called once. The options passed to the additional call (${JSON.stringify(options)}) will be ignored.`;
var MSG_IMPORT_LIBRARY_EXISTS = (options) => `The google.maps.importLibrary() function is already defined, and @googlemaps/js-api-loader will use the existing function instead of overwriting it. The options passed to setOptions (${JSON.stringify(options)}) will be ignored.`;
var MSG_SET_OPTIONS_NOT_CALLED = "No options were set before calling importLibrary. Make sure to configure the loader using setOptions().";
var MSG_SCRIPT_ELEMENT_EXISTS = "There already is a script loading the Google Maps JavaScript API, and no google.maps.importLibrary function is defined. @googlemaps/js-api-loader will proceed to bootstrap the API with the specified options, but the existing script might cause problems using the API. Make sure to remove the script loading the API.";
var logDevWarning = (message) => {
	console.warn(`[@googlemaps/js-api-loader] ${message}`);
};
var logDevNotice = (message) => {
	console.info(`[@googlemaps/js-api-loader] ${message}`);
};
/**
* @deprecated Use the new functional API: `setOptions()` and `importLibrary()`.
* See the migration guide for more details: MIGRATION.md
*/
var Loader = class {
	constructor(...args) {
		throw new Error(`[@googlemaps/js-api-loader]: ${MSG_DEPRECATED_LOADER}`);
	}
};
var setOptionsWasCalled_ = false;
/**
* Sets the options for the Maps JavaScript API.
*
* Has to be called before any library is loaded.
*
* See https://developers.google.com/maps/documentation/javascript/load-maps-js-api#required_parameters
* for the full documentation of available options.
*
* @param options The options to set.
*/
function setOptions(options) {
	if (setOptionsWasCalled_) {
		logDevWarning(MSG_REPEATED_SET_OPTIONS(options));
		return;
	}
	installImportLibrary_(options);
	setOptionsWasCalled_ = true;
}
async function importLibrary(libraryName) {
	if (!setOptionsWasCalled_) logDevWarning(MSG_SET_OPTIONS_NOT_CALLED);
	if (!window?.google?.maps?.importLibrary) throw new Error("google.maps.importLibrary is not installed.");
	return await google.maps.importLibrary(libraryName);
}
/**
* The installImportLibrary_ function makes sure that a usable version of the
* `google.maps.importLibrary` function exists.
*/
function installImportLibrary_(options) {
	const importLibraryExists = Boolean(window.google?.maps?.importLibrary);
	if (importLibraryExists) logDevNotice(MSG_IMPORT_LIBRARY_EXISTS(options));
	else if (document.querySelector("script[src*=\"maps.googleapis.com/maps/api/js\"]")) logDevWarning(MSG_SCRIPT_ELEMENT_EXISTS);
	if (!importLibraryExists) bootstrap(options);
}
//#endregion
export { Loader, importLibrary, setOptions };

//# sourceMappingURL=@googlemaps_js-api-loader.js.map