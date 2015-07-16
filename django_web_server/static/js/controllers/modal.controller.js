function ModalController($rootScope, $scope) {

	$scope.$parent.modalController = this;

	$scope.showModal = false;
	
	$scope.button1Text = 'one';
	$scope.onButton1 = function() {};

	$scope.button2Text = 'two';
	$scope.onButton2 = function() {};

	$scope.openModal = function() {
		$scope.showModal = true;
	};

	$scope.click1 = function() { 
		$scope.onButton1(); 
		$scope.showModal = false; 
	};
	$scope.click2 = function() { 
		$scope.onButton2();
		$scope.showModal = false; 
	};

	$scope.openUnsavedChangesModal = function(onSave, onDiscard) {
		

		$scope.modalTitle = 'Stand @ ' + $scope.model.selectedProperty.name;

		$scope.cancel = 'cancel';
		$scope.button1Text = 'save';
		$scope.onButton1 = onSave;
		$scope.button2Text = 'discard';
		$scope.onButton2 = onDiscard;

		$scope.showModal = true;
	};

	$rootScope.$on(Command.OPEN_UNSAVED_CHANGES_MODAL, function(evt, data){
		$scope.openUnsavedChangesModal(data.onSave, data.onDiscard);
	});

	$scope.closeModal = function() {
		$scope.showModal = false;
	};

	this.openModal = function() {
		$scope.openUnsavedChangesModal();
	};
}