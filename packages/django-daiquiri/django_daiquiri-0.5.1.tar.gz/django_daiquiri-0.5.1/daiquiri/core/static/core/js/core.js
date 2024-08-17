angular.module('core', ['ngResource', 'ngSanitize'])

.config(['$httpProvider', '$interpolateProvider', '$resourceProvider', function($httpProvider, $interpolateProvider, $resourceProvider) {

    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    $resourceProvider.defaults.stripTrailingSlashes = false;
    $resourceProvider.defaults.actions.update = {
        method: 'PUT',
        params: {}
    };
    $resourceProvider.defaults.actions.paginate = {
        method: 'GET',
        isArray: false
    };
}])

.directive('codemirror', function() {
    return {
        scope: {
            id: '@',
            model: '='
        },
        require: 'ngModel',
        link: function(scope, element, attrs, ngModel) {
            // instanciate CodeMirror on the element
            scope.editor = CodeMirror.fromTextArea(element[0], {
                lineNumbers: true,
                lineWrapping: true,
                mode: attrs.mode
            });

            // whenever the user types into code mirror update the model
            scope.editor.on('change', function(cm, change) {
                ngModel.$setViewValue(cm.getValue());
            });

            // when the model is updated update codemirror
            ngModel.$formatters.push(function(model_values) {

                if (angular.isDefined(model_values) && model_values) {
                    scope.editor.setValue(model_values);
                } else {
                    scope.editor.setValue('');
                }
                return model_values;
            });
        }
    };
})

.directive('pending', ['$http', '$timeout', function ($http, $timeout) {
    return {
        restrict: 'E',
        template: '<i class="fa fa-circle-o-notch fa-spin fa-fw"></i>',
        link: function (scope, element, attrs) {
            scope.isPending = function () {
                return $http.pendingRequests.length > 0;
            };
            scope.$watch(scope.isPending, function (value) {
                if (value) {
                    if (angular.isUndefined(scope.promise) || scope.pending === null) {
                        scope.promise = $timeout(function(){
                            element.removeClass('ng-hide');
                        }, 500);
                    }
                } else {
                    $timeout.cancel(scope.promise);
                    scope.pending = null;
                    element.addClass('ng-hide');
                }
            });
        }
    };
}])

.directive('fileInput', function() {
    return {
        restrict: 'C',
        require: 'ngModel',
        link: function (scope, elem, attrs, ngModel) {
            elem.on('change', function(e) {
                var file = elem[0].files[0];
                ngModel.$setViewValue(file);
            })
        }
    }
})

.directive('dateInput', ['$timeout', function($timeout) {
    return {
        restrict: 'C',
        require: 'ngModel',
        link: function(scope, element, attrs, ngModelController) {
            ngModelController.$parsers.push(function(view_value) {
                if (view_value === null) {
                    return null
                } else {
                    return [
                        view_value.getFullYear(),
                        ('0' + (view_value.getMonth() + 1)).slice(-2),
                        ('0' + view_value.getDate()).slice(-2)
                    ].join('-');
                }
            });

            ngModelController.$formatters.push(function(model_value) {
                if (model_value === null) {
                    return null
                } else {
                    return new Date(model_value);
                }
            });
        }
    };
}])

.directive('splitLines', function() {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function(scope, element, attrs, ngModelController) {
            ngModelController.$parsers.push(function(view_value) {
                if (view_value === null) {
                    return null
                } else {
                    return view_value.split("\n")
                }
            });

            ngModelController.$formatters.push(function(model_value) {
                if (model_value === null) {
                    return null
                } else {
                    return model_value.join("\n");
                }
            });
        }
    };
})
;
