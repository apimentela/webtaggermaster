var EasyAutocomplete = (function(scope){
	scope.Template = function Template(options) {
		var genericTemplates = {
			basic: {
				type: "basic",
				method: function(element) { return element; },
				cssClass: ""
			},
			description: {
				type: "description",
				fields: {
					description: "description"
				},
				method: function(element) {	return element + " - description"; },
				cssClass: "eac-description"
			},
			iconLeft: {
				type: "iconLeft",
				fields: {
					icon: ""
				},
				method: function(element) {
					return element;
				},
				cssClass: "eac-icon-left"
			},
			iconRight: {
				type: "iconRight",
				fields: {
					iconSrc: ""
				},
				method: function(element) {
					return element;
				},
				cssClass: "eac-icon-right"
			},
			links: {
				type: "links",
				fields: {
					link: ""
				},
				method: function(element) {
					return element;
				},
				cssClass: ""
			},
			custom: {
				type: "custom",
				method: function() {},
				cssClass: ""
			}
		},
		convertTemplateToMethod = function(template) {
			var _fields = template.fields,
				buildMethod;
			if (template.type === "description") {
				buildMethod = genericTemplates.description.method; 
				if (typeof _fields.description === "string") {
					buildMethod = function(elementValue, element) {
						return elementValue + " - <span>" + element[_fields.description] + "</span>";
					};					
				} else if (typeof _fields.description === "function") {
					buildMethod = function(elementValue, element) {
						return elementValue + " - <span>" + _fields.description(element) + "</span>";
					};	
				}
				return buildMethod;
			}
			if (template.type === "iconRight") {
				if (typeof _fields.iconSrc === "string") {
					buildMethod = function(elementValue, element) {
						return elementValue + "<img class='eac-icon' src='" + element[_fields.iconSrc] + "' />" ;
					};					
				} else if (typeof _fields.iconSrc === "function") {
					buildMethod = function(elementValue, element) {
						return elementValue + "<img class='eac-icon' src='" + _fields.iconSrc(element) + "' />" ;
					};
				}
				return buildMethod;
			}
			if (template.type === "iconLeft") {
				if (typeof _fields.iconSrc === "string") {
					buildMethod = function(elementValue, element) {
						return "<img class='eac-icon' src='" + element[_fields.iconSrc] + "' />" + elementValue;
					};					
				} else if (typeof _fields.iconSrc === "function") {
					buildMethod = function(elementValue, element) {
						return "<img class='eac-icon' src='" + _fields.iconSrc(element) + "' />" + elementValue;
					};
				}
				return buildMethod;
			}
			if(template.type === "links") {
				if (typeof _fields.link === "string") {
					buildMethod = function(elementValue, element) {
						return "<a href='" + element[_fields.link] + "' >" + elementValue + "</a>";
					};					
				} else if (typeof _fields.link === "function") {
					buildMethod = function(elementValue, element) {
						return "<a href='" + _fields.link(element) + "' >" + elementValue + "</a>";
					};
				}
				return buildMethod;
			}
			if (template.type === "custom") {
				return template.method;
			}
			return genericTemplates.basic.method;
		},
		prepareBuildMethod = function(options) {
			if (!options || !options.type) {
				return genericTemplates.basic.method;
			}
			if (options.type && genericTemplates[options.type]) {
				return convertTemplateToMethod(options);
			} else {
				return genericTemplates.basic.method;
			}
		},
		templateClass = function(options) {
			var emptyStringFunction = function() {return "";};
			if (!options || !options.type) {
				return emptyStringFunction;
			}
			if (options.type && genericTemplates[options.type]) {
				return (function () { 
					var _cssClass = genericTemplates[options.type].cssClass;
					return function() { return _cssClass;};
				})();
			} else {
				return emptyStringFunction;
			}
		};
		this.getTemplateClass = templateClass(options);
		this.build = prepareBuildMethod(options);
	};
	return scope;
})(EasyAutocomplete || {});
