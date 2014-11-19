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
  var loadEgos = $q.defer();
  
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
  
  $http({url: baseUrl + 'egos.json'})
    .success(function (data) {
      loadEgos.resolve(data);
    });
  
  $q.all([loadNodes.promise, loadResults.promise, loadEgos.promise])
    .then(function(values) {
      // make dict of ego values
      var egoDict = {};
      values[2].forEach(function(d) {
        egoDict[d.id] = d.list;
      })
          
      $scope.playerList.forEach(function(player) {
        // assign ego results
        player.egos = egoDict[player.id];
        // replace id with name
        player.id = $scope.nodes[player.id];
        // same for player's list
        player.list.forEach(function(sim) {
          sim.n = $scope.nodes[sim.n];
        });
      });
    });
});