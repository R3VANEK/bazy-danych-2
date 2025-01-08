$(document).on('click', '.delete-vehicle', function() {
    deleteVehicleRequest($(this).data('vehicle-id'));
    getVehicleList();
});

$(document).on('click', '.edit-vehicle', function() {
    const vehicleId = $(this).data('vehicle-id');
    fetchVehicleData(vehicleId);
    
    $('#edit-vehicle-modal').removeClass('hidden');
    $('body').addClass('blurred');
});

$(document).on('click', '#add-vehicle', function() {
    $('#add-vehicle-modal').removeClass('hidden');
    $('body').addClass('blurred');
});

$('#cancel-modal').on('click', function() {
    $('#add-vehicle-modal').addClass('hidden');
    $('body').removeClass('blurred');
});

$('#confirm-add-modal').on('click', function(){
    addVehicleRequest();
    $('#add-vehicle-modal').addClass('hidden');
    $('body').removeClass('blurred');
});

$('#confirm-edit-modal').on('click', function(){
    let vehicleId = $("#confirm-edit-modal").data("vehicle-id");
    let maxPassengers = $("#edit-vehicle-max-passengers").val();
    let name = $("#edit-vehicle-name").val();
    editVehicleRequest(vehicleId, name, maxPassengers);
    $('#edit-vehicle-modal').addClass('hidden');
    $('body').removeClass('blurred');
});

$('#cancel-edit-modal').on('click', function() {
    $('#edit-vehicle-modal').addClass('hidden');
    $('body').removeClass('blurred');
});

function editVehicleRequest(vehicleId, name, maxPassengers){
    const csrfToken = getCSRFToken();
    const editVehicleUrl = edit_vehicle_url; // Zmienna powinna być przekazana do JS

    fetch(editVehicleUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
           id: vehicleId,
           name: name,
           maxPassengers: maxPassengers
        })
    })
    .then(response => response.json())
    .then(response => {
        Toastify({
                text: response.text,
                duration:3000,
                style: {
                    background: (response.type == "success") ? "green" : "red",
                }
            }).showToast()

        getVehicleList();
    });
}

function fetchVehicleData(vehicleId) {
    const csrfToken = getCSRFToken();
    const getVehicleUrl = get_vehicle_url; // Zmienna powinna być przekazana do JS

    fetch(getVehicleUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
           id: vehicleId,
        })
    })
    .then(response => response.json())
    .then(vehicles => {
        $('#edit-vehicle-name').val(vehicles[0].name);
        $('#edit-vehicle-max-passengers').val(vehicles[0].max_passengers);
        console.log(vehicles[0].id);
        $('#confirm-edit-modal').attr('data-vehicle-id', vehicles[0].id);
    });
}

function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === 'csrftoken') {
            return decodeURIComponent(value);
        }
    }
    return null;
}

function generateVehicleHTML(vehicles){
    return vehicles.map(vehicle => `
        <div class="travel-card !h-[10rem]">
            <div class="flex items-center mt-1">
                <i class="fa-brands fa-space-awesome"></i>
                <p class="ml-4">${vehicle.name}</p>
            </div>

            <div class="flex items-center mt-1">
                <i class="fa-solid fa-fingerprint"></i>
                <p class="ml-4">${vehicle.registration_number}</p>
            </div>

            <div class="flex items-center mt-1">
                <i class="fa-solid fa-person"></i>
                <p class="ml-4">${vehicle.max_passengers} max passengers</p>
            </div>

            <div class="edit-vehicle absolute bottom-12 -right-4 bg-cosmic-purple p-4 text-white font-thin text-xl cursor-pointer" data-vehicle-id="${vehicle.id}">
                <i class="fa-solid fa-edit"></i>
            </div>

            <div class="delete-vehicle absolute -bottom-4 -right-4 bg-danger p-4 text-white font-thin text-xl cursor-pointer" data-vehicle-id="${vehicle.id}">
                <i class="fa-solid fa-trash"></i>
            </div>
        </div>
    `).join('');
}

function updateVehiclesList(vehicles) {
    const coursesContainer = $('#vehicles-holder');
    const newCoursesHTML = generateVehicleHTML(vehicles);
    coursesContainer.html(newCoursesHTML);
}

function getVehicleList(){
    const csrfToken = getCSRFToken();
    const getVehiclesUrl = get_vehicles_url; // Zmienna powinna być przekazana do JS

    fetch(getVehiclesUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({})
    })
    .then((response) => response.json())
    .then((response) => {
        updateVehiclesList(response);
    });
}

function addVehicleRequest(){
    let addVehicleUrl = add_vehicle_url; // Zmienna powinna być przekazana do JS
    const csrfToken = getCSRFToken();

    const name = $('#add-vehicle-name').val();
    const registrationNumber = $('#add-vehicle-registration-number').val();
    const maxPassengers = $('#add-vehicle-max-passengers').val();

    fetch(addVehicleUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
           name: name,
           registrationNumber: registrationNumber,
           maxPassengers: maxPassengers
        })
    })
    .then((response) => response.json())
    .then((response) => {
        Toastify({
                text: response.text,
                duration:3000,
                style: {
                    background: (response.type == "success") ? "green" : "red",
                }
            }).showToast()

        getVehicleList();
    });
}

function deleteVehicleRequest(vehicleId){
    let deleteVehicleUrl = delete_vehicle_url; // Zmienna powinna być przekazana do JS
    const csrfToken = getCSRFToken();

    if(!vehicleId){
        Toastify({
                text: "Please select vehicle to delete!",
                duration:3000,
                style: {
                    background: "red",
                }
            }).showToast();
        return;
    }

    fetch(deleteVehicleUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
           id: vehicleId,
        })
    })
    .then((response) => response.json())
    .then((response) => {
        Toastify({
                text: response.text,
                duration:3000,
                style: {
                    background: (response.type == "success") ? "green" : "red",
                }
            }).showToast();
        getVehicleList(); // Dodane odświeżenie listy po usunięciu
    });
}

// Inicjalizacja listy pojazdów przy załadowaniu strony
$(document).ready(function(){
    getVehicleList();
});