let courseId = null;

// Obsługa kliknięcia na przycisk ceny kursu
$(document).on('click', '.price-click', function() {
    courseId = $(this).data('course-id');
    $('#course-modal').removeClass('hidden');
    $('body').addClass('blurred');
});

// Obsługa kliknięcia na przycisk anulowania modala
$('#cancel-modal').on('click', function() {
    $('#course-modal').addClass('hidden');
    $('body').removeClass('blurred');
});

// Obsługa kliknięcia na przycisk potwierdzenia rezerwacji
$('#confirm-modal').on('click', bookRideRequest);

// Zamknięcie modala po kliknięciu poza jego zawartością
$('#course-modal').on('click', function(e) {
    if ($(e.target).is('#course-modal')) {
        $('#course-modal').addClass('hidden');
        $('body').removeClass('blurred');
    }
});

// Inicjalizacja DatePicker dla pola daty wyjazdu
$(function() {
    $("#time-for-departure").datepicker({
        beforeShow: function(){
            setTimeout(function(){
                $('.ui-datepicker').css('z-index', 99999999999999);
            }, 0);
        }
    });
});

// Funkcja debounce do ograniczenia liczby wywołań funkcji
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
}

// Funkcja do pobierania CSRF tokena z ciasteczek
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

// Funkcja generująca HTML dla listy kursów
function generateCourseHTML(courses) {
    return courses.map(course => {
        return `
            <div class="travel-card">
                <div class="flex items-center">
                    <i class="fa-solid fa-user text-3xl"></i>
                    <p class="text-4xl ml-4">${course.driver_name}</p>
                </div>

                <div class="flex items-center mt-1">
                    <i class="fa-solid fa-star"></i>
                    <p class="ml-4">${parseFloat(course.driver_grade).toFixed(2)} / 5.00</p>
                </div>

                <div class="flex items-center mt-1">
                    <i class="fa-solid fa-clock"></i>
                    <p class="ml-4">${new Date(course.start_date).toLocaleDateString('en-GB')}</p>
                </div>

                <div class="flex items-center mt-1">
                    <i class="fa-solid fa-clock"></i>
                    <p class="ml-4">${course.duration_days} days</p>
                </div>

                <div class="flex items-center mt-1">
                    <i class="fa-solid fa-circle"></i>
                    <p class="ml-4">to ${course.destination_name}</p>
                </div>

                <div class="flex items-center mt-1">
                    <i class="fa-solid fa-person"></i>
                    <p class="ml-4">${course.taken_seats} / ${course.max_seats} seats left</p>
                </div>
                
                <div class="price-click absolute -bottom-4 -right-4 bg-cosmic-purple p-6 text-white font-thin text-3xl cursor-pointer" data-course-id="${course.id}">${course.price} TIX</div>
            </div>
        `;
    }).join('');
}

// Funkcja aktualizująca listę kursów na stronie
function updateCourseList(courses) {
    const coursesContainer = $('#courses-holder');
    const newCoursesHTML = generateCourseHTML(courses);
    coursesContainer.html(newCoursesHTML);
}

// Funkcja obsługująca rezerwację kursu
function bookRideRequest(){
    let getCoursesFetch = book_ride_url; // URL zdefiniowany w szablonie
    const csrfToken = getCSRFToken();

    const selectedPlanetId = $('#planet-select').val();

    if(!selectedPlanetId || !courseId){
        Toastify({
                text: "Departure planet or course is not selected!",
                duration:3000,
                style: {
                    background: "red",
                }
            }).showToast()
        return
    }

    fetch(getCoursesFetch, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            departureId: selectedPlanetId,
            courseId: courseId
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

        getCoursesFilter(true);
        $('#course-modal').addClass('hidden');
        $('body').removeClass('blurred');
    });
}

// Funkcja pobierająca kursy z filtrem
function getCoursesFilter(pure_refresh = false) {
    const destination = (!pure_refresh) ? $('#destination').val() : null;
    const driverGender = (!pure_refresh) ? $('#gender-driver').val() : null;
    const timeForDeparture = (!pure_refresh) ? $('#time-for-departure').val() : null;
    const grade = (!pure_refresh) ? $('#grade').val() : null;
    const maxPrice = (!pure_refresh) ? $('#max-price').val() : null;

    let getCoursesFetch = get_courses_url; // URL zdefiniowany w szablonie
    const csrfToken = getCSRFToken();

    fetch(getCoursesFetch, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            destination: destination,
            driverGender: driverGender,
            timeForDeparture: timeForDeparture,
            grade: grade,
            maxPrice: maxPrice
        })
    })
    .then((response) => response.json())
    .then((response) => {
        updateCourseList(response);
    });
}

// Funkcja debounce do ograniczenia liczby wywołań funkcji
const debouncedGetCoursesFilter = debounce(getCoursesFilter, 500);

// Powiązanie filtrów z funkcją pobierającą kursy
$('#destination').on('change', debouncedGetCoursesFilter);
$('#gender-driver').on('change', debouncedGetCoursesFilter);
$('#time-for-departure').on('change', debouncedGetCoursesFilter);
$('#grade').on('change', debouncedGetCoursesFilter);
$('#max-price').on('change', debouncedGetCoursesFilter);