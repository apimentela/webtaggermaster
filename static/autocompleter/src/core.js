var EasyAutocomplete = (function(scope) {
	scope.main = function Core($input, options) {
		var module = {
				name: "EasyAutocomplete",
				shortcut: "eac"
			};
		var consts = new scope.Constans(),
			config = new scope.Configuration(options),
			logger = new scope.Logger(),
			template = new scope.Template(options.template),
			listBuilderService = new scope.ListBuilderService(config, scope.proccess),
			checkParam = config.equals,
			$field = $input, 
			$container = "",
			elementsList = [],
			selectedElement = -1,
			requestDelayTimeoutId;
		scope.consts = consts;
		this.getConstants = function() {
			return consts;
		};
		this.getConfiguration = function() {
			return config;
		};
		this.getContainer = function() {
			return $container;
		};
		this.getSelectedItemIndex = function() {
			return selectedElement;
		};
		this.getItems = function () {
			return elementsList;
		};
		this.getItemData = function(index) {
			if (elementsList.length < index || elementsList[index] === undefined) {
				return -1;
			} else {
				return elementsList[index];
			}
		};
		this.getSelectedItemData = function() {
			return this.getItemData(selectedElement);
		};
		this.build = function() {
			prepareField();
		};
		this.init = function() {
			init();
		};
		function init() {
			if ($field.length === 0) {
				logger.error("Input field doesn't exist.");
				return;
			}
			if (!config.checkDataUrlProperties()) {
				logger.error("One of options variables 'data' or 'url' must be defined.");
				return;
			}
			if (!config.checkRequiredProperties()) {
				logger.error("Will not work without mentioned properties.");
				return;
			}
			prepareField();
			bindEvents();	
		}
		function prepareField() {
			if ($field.parent().hasClass(consts.getValue("WRAPPER_CSS_CLASS"))) {
				removeContainer();
				removeWrapper();
			} 
			createWrapper();
			createContainer();	
			$container = $("#" + getContainerId());
			if (config.get("placeholder")) {
				$field.attr("placeholder", config.get("placeholder"));
			}
			function createWrapper() {
				var $wrapper = $("<div>"),
					classes = consts.getValue("WRAPPER_CSS_CLASS");
				if (config.get("theme") && config.get("theme") !== "") {
					classes += " eac-" + config.get("theme");
				}
				if (config.get("cssClasses") && config.get("cssClasses") !== "") {
					classes += " " + config.get("cssClasses");
				}
				if (template.getTemplateClass() !== "") {
					classes += " " + template.getTemplateClass();
				}
				$wrapper
					.addClass(classes);
				$field.wrap($wrapper);
				if (config.get("adjustWidth") === true) {
					adjustWrapperWidth();	
				}
			}
			function adjustWrapperWidth() {
				var fieldWidth = $field.outerWidth();
				$field.parent().css("width", fieldWidth);				
			}
			function removeWrapper() {
				$field.unwrap();
			}
			function createContainer() {
				var $elements_container = $("<div>").addClass(consts.getValue("CONTAINER_CLASS"));
				$elements_container
						.attr("id", getContainerId())
						.prepend($("<ul>"));
				(function() {
					$elements_container
						.on("show.eac", function() {
							switch(config.get("list").showAnimation.type) {
								case "slide":
									var animationTime = config.get("list").showAnimation.time,
										callback = config.get("list").showAnimation.callback;
									$elements_container.find("ul").slideDown(animationTime, callback);
								break;
								case "fade":
									var animationTime = config.get("list").showAnimation.time,
										callback = config.get("list").showAnimation.callback;
									$elements_container.find("ul").fadeIn(animationTime), callback;
								break;
								default:
									$elements_container.find("ul").show();
								break;
							}
							config.get("list").onShowListEvent();
						})
						.on("hide.eac", function() {
							switch(config.get("list").hideAnimation.type) {
								case "slide":
									var animationTime = config.get("list").hideAnimation.time,
										callback = config.get("list").hideAnimation.callback;
									$elements_container.find("ul").slideUp(animationTime, callback);
								break;
								case "fade":
									var animationTime = config.get("list").hideAnimation.time,
										callback = config.get("list").hideAnimation.callback;
									$elements_container.find("ul").fadeOut(animationTime, callback);
								break;
								default:
									$elements_container.find("ul").hide();
								break;
							}
							config.get("list").onHideListEvent();
						})
						.on("selectElement.eac", function() {
							$elements_container.find("ul li").removeClass("selected");
							$elements_container.find("ul li").eq(selectedElement).addClass("selected");
							config.get("list").onSelectItemEvent();
						})
						.on("loadElements.eac", function(event, listBuilders, phrase) {
							var $item = "",
								$listContainer = $elements_container.find("ul");
							$listContainer
								.empty()
								.detach();
							elementsList = [];
							var counter = 0;
							for(var builderIndex = 0, listBuildersLength = listBuilders.length; builderIndex < listBuildersLength; builderIndex += 1) {
								var listData = listBuilders[builderIndex].data;
								if (listData.length === 0) {
									continue;
								}
								if (listBuilders[builderIndex].header !== undefined && listBuilders[builderIndex].header.length > 0) {
									$listContainer.append("<div class='eac-category' >" + listBuilders[builderIndex].header + "</div>");
								}
								for(var i = 0, listDataLength = listData.length; i < listDataLength && counter < listBuilders[builderIndex].maxListSize; i += 1) {
									$item = $("<li><div class='eac-item'></div></li>");
									(function() {
										var j = i,
											itemCounter = counter,
											elementsValue = listBuilders[builderIndex].getValue(listData[j]);
										$item.find(" > div")
											.on("click", function() {
												$field.val(elementsValue).trigger("change");
												selectedElement = itemCounter;
												selectElement(itemCounter);
												config.get("list").onClickEvent();
												config.get("list").onChooseEvent();
											})
											.mouseover(function() {
												selectedElement = itemCounter;
												selectElement(itemCounter);	
												config.get("list").onMouseOverEvent();
											})
											.mouseout(function() {
												config.get("list").onMouseOutEvent();
											})
											.html(template.build(highlight(elementsValue, phrase), listData[j]));
									})();
									$listContainer.append($item);
									elementsList.push(listData[i]);
									counter += 1;
								}
							}
							$elements_container.append($listContainer);
							config.get("list").onLoadEvent();
						});
				})();
				$field.after($elements_container);
			}
			function removeContainer() {
				$field.next("." + consts.getValue("CONTAINER_CLASS")).remove();
			}
			function highlight(string, phrase) {
				if(config.get("highlightPhrase") && phrase !== "") {
					return highlightPhrase(string, phrase);	
				} else {
					return string;
				}
			}
			function escapeRegExp(str) {
				return str.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, "\\$&");
 			}
			function highlightPhrase(string, phrase) {
				var escapedPhrase = escapeRegExp(phrase);
				return (string + "").replace(new RegExp("(" + escapedPhrase + ")", "gi") , "<b>$1</b>");
			}
		}
		function getContainerId() {
			var elementId = $field.attr("id");
			elementId = consts.getValue("CONTAINER_ID") + elementId;
			return elementId;
		}
		function bindEvents() {
			bindAllEvents();
			function bindAllEvents() {
				if (checkParam("autocompleteOff", true)) {
					removeAutocomplete();
				}
				bindFocusOut();
				bindKeyup();
				bindKeydown();
				bindKeypress();
				bindFocus();
				bindBlur();
			}
			function bindFocusOut() {
				$field.focusout(function () {
					var fieldValue = $field.val(),
						phrase;
					if (!config.get("list").match.caseSensitive) {
						fieldValue = fieldValue.toLowerCase();
					}
					for (var i = 0, length = elementsList.length; i < length; i += 1) {
						phrase = config.get("getValue")(elementsList[i]);
						if (!config.get("list").match.caseSensitive) {
							phrase = phrase.toLowerCase();
						}
						if (phrase === fieldValue) {
							selectedElement = i;
							selectElement(selectedElement);
							return;
						}
					}
				});
			}
			function bindKeyup() {
				$field
				.off("keyup")
				.keyup(function(event) {
					switch(event.keyCode) {
						case 27:
							hideContainer();
							loseFieldFocus();
						break;
						case 38:
							event.preventDefault();
							if(elementsList.length > 0 && selectedElement > 0) {
								selectedElement -= 1;
								$field.val(config.get("getValue")(elementsList[selectedElement]));
								selectElement(selectedElement);
							}						
						break;
						case 40:
							event.preventDefault();
							if(elementsList.length > 0 && selectedElement < elementsList.length - 1) {
								selectedElement += 1;
								$field.val(config.get("getValue")(elementsList[selectedElement]));
								selectElement(selectedElement);
							}
						break;
						default:
							if (event.keyCode > 40 || event.keyCode === 8) {
								var inputPhrase = $field.val();
								if (!(config.get("list").hideOnEmptyPhrase === true && event.keyCode === 8 && inputPhrase === "")) {
									if (config.get("requestDelay") > 0) {
										if (requestDelayTimeoutId !== undefined) {
											clearTimeout(requestDelayTimeoutId);
										}
										requestDelayTimeoutId = setTimeout(function () { loadData(inputPhrase);}, config.get("requestDelay"));
									} else {
										loadData(inputPhrase);
									}
								} else {
									hideContainer();
								}
							}
						break;
					}
					function loadData(inputPhrase) {
						if (inputPhrase.length < config.get("minCharNumber")) {
							return;
						}
						if (config.get("data") !== "list-required") {
							var data = config.get("data");
							var listBuilders = listBuilderService.init(data);
							listBuilders = listBuilderService.updateCategories(listBuilders, data);
							listBuilders = listBuilderService.processData(listBuilders, inputPhrase);
							loadElements(listBuilders, inputPhrase);
							if ($field.parent().find("li").length > 0) {
								showContainer();	
							} else {
								hideContainer();
							}
						}
						var settings = createAjaxSettings();
						if (settings.url === undefined || settings.url === "") {
							settings.url = config.get("url");
						}
						if (settings.dataType === undefined || settings.dataType === "") {
							settings.dataType = config.get("dataType");
						}
						if (settings.url !== undefined && settings.url !== "list-required") {
							settings.url = settings.url(inputPhrase);
							settings.data = config.get("preparePostData")(settings.data, inputPhrase);
							$.ajax(settings) 
								.done(function(data) {
									var listBuilders = listBuilderService.init(data);
									listBuilders = listBuilderService.updateCategories(listBuilders, data);
									listBuilders = listBuilderService.convertXml(listBuilders);
									if (checkInputPhraseMatchResponse(inputPhrase, data)) {
										listBuilders = listBuilderService.processData(listBuilders, inputPhrase);
										loadElements(listBuilders, inputPhrase);	
									}
									if (listBuilderService.checkIfDataExists(listBuilders) && $field.parent().find("li").length > 0) {
										showContainer();	
									} else {
										hideContainer();
									}
									config.get("ajaxCallback")();
								})
								.fail(function() {
									logger.warning("Fail to load response data");
								})
								.always(function() {
								});
						}
						function createAjaxSettings() {
							var settings = {},
								ajaxSettings = config.get("ajaxSettings") || {};
							for (var set in ajaxSettings) {
								settings[set] = ajaxSettings[set];
							}
							return settings;
						}
						function checkInputPhraseMatchResponse(inputPhrase, data) {
							if (config.get("matchResponseProperty") !== false) {
								if (typeof config.get("matchResponseProperty") === "string") {
									return (data[config.get("matchResponseProperty")] === inputPhrase);
								}
								if (typeof config.get("matchResponseProperty") === "function") {
									return (config.get("matchResponseProperty")(data) === inputPhrase);
								}
								return true;
							} else {
								return true;
							}
						}
					}
				});
			}
			function bindKeydown() {
				$field
					.on("keydown", function(evt) {
	        		    evt = evt || window.event;
	        		    var keyCode = evt.keyCode;
	        		    if (keyCode === 38) {
	        		        suppressKeypress = true; 
	        		        return false;
	        		    }
		        	})
					.keydown(function(event) {
						if (event.keyCode === 13 && selectedElement > -1) {
							$field.val(config.get("getValue")(elementsList[selectedElement]));
							config.get("list").onKeyEnterEvent();
							config.get("list").onChooseEvent();
							selectedElement = -1;
							hideContainer();
							event.preventDefault();
						}
					});
			}
			function bindKeypress() {
				$field
				.off("keypress");
			}
			function bindFocus() {
				$field.focus(function() {
					if ($field.val() !== "" && elementsList.length > 0) {
						selectedElement = -1;
						showContainer();	
					}
				});
			}
			function bindBlur() {
				$field.blur(function() {
					setTimeout(function() { 
						selectedElement = -1;
						hideContainer();
					}, 250);
				});
			}
			function removeAutocomplete() {
				$field.attr("autocomplete","off");
			}
		}
		function showContainer() {
			$container.trigger("show.eac");
		}
		function hideContainer() {
			$container.trigger("hide.eac");
		}
		function selectElement(index) {
			$container.trigger("selectElement.eac", index);
		}
		function loadElements(list, phrase) {
			$container.trigger("loadElements.eac", [list, phrase]);
		}
		function loseFieldFocus() {
			$field.trigger("blur");
		}
	};
	scope.eacHandles = [];
	scope.getHandle = function(id) {
		return scope.eacHandles[id];
	};
	scope.inputHasId = function(input) {
		if($(input).attr("id") !== undefined && $(input).attr("id").length > 0) {
			return true;
		} else {
			return false;
		}
	};
	scope.assignRandomId = function(input) {
		var fieldId = "";
		do {
			fieldId = "eac-" + Math.floor(Math.random() * 10000);		
		} while ($("#" + fieldId).length !== 0);
		elementId = scope.consts.getValue("CONTAINER_ID") + fieldId;
		$(input).attr("id", fieldId);
	};
	scope.setHandle = function(handle, id) {
		scope.eacHandles[id] = handle;
	};
	return scope;
})(EasyAutocomplete || {});
(function($) {
	$.fn.easyAutocomplete = function(options) {
		return this.each(function() {
			var $this = $(this),
				eacHandle = new EasyAutocomplete.main($this, options);
			if (!EasyAutocomplete.inputHasId($this)) {
				EasyAutocomplete.assignRandomId($this);
			}
			eacHandle.init();
			EasyAutocomplete.setHandle(eacHandle, $this.attr("id"));
		});
	};
	$.fn.getSelectedItemIndex = function() {
		var inputId = $(this).attr("id");
		if (inputId !== undefined) {
			return EasyAutocomplete.getHandle(inputId).getSelectedItemIndex();
		}
		return -1;
	};
	$.fn.getItems = function () {
		var inputId = $(this).attr("id");
		if (inputId !== undefined) {
			return EasyAutocomplete.getHandle(inputId).getItems();
		}
		return -1;
	};
	$.fn.getItemData = function(index) {
		var inputId = $(this).attr("id");
		if (inputId !== undefined && index > -1) {
			return EasyAutocomplete.getHandle(inputId).getItemData(index);
		}
		return -1;
	};
	$.fn.getSelectedItemData = function() {
		var inputId = $(this).attr("id");
		if (inputId !== undefined) {
			return EasyAutocomplete.getHandle(inputId).getSelectedItemData();
		}
		return -1;
	};
})(jQuery);
