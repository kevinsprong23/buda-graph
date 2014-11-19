angular.module('BudaApp.controllers', [])
.controller('playerController', function($scope, $http, $q) {
  $scope.nodes = {};
  $scope.playerList = [];
  
  $scope.searchFilter = function (player) {
    var re = new RegExp($scope.nameFilter, 'i');
    return $scope.nameFilter && $scope.nameFilter.length > 4 && re.test(player.id);
  };
  
  // async load
  var baseUrl = '';
  
  var loadNodes = $q.defer();
  var loadResults = $q.defer();
  
  $http({url: baseUrl + 'nodes.json'})
    .success(function (data) {
      data.forEach(function(node) {
        $scope.nodes[node.id] = node.label;
      });
      loadNodes.resolve(data);
    });
  
  $http({url: baseUrl + 'similarities.json'})
    .success(function (data) {
      $scope.playerList = data;
      loadResults.resolve(data);
    });
  
  $q.all([loadNodes.promise, loadResults.promise])
    .then(function(values) {
      $scope.playerList.forEach(function(player) {
        // replace id with name
        player.id = $scope.nodes[player.id];
        // same for player's list
        player.list.forEach(function(sim) {
          sim.n = $scope.nodes[sim.n];
        });
      });
    });
});