// ==============================Password Toggle===========================================//
function togglePasswordVisibility() {
  const passwordInput = document.getElementById('password');
  const toggleIcon = document.getElementById('toggleIcon');
  if (passwordInput.type === 'password') {
      passwordInput.type = 'text';
      toggleIcon.classList.remove('fa-eye-slash');
      toggleIcon.classList.add('fa-eye');
  } else {
      passwordInput.type = 'password';
      toggleIcon.classList.remove('fa-eye');
      toggleIcon.classList.add('fa-eye-slash');
  }
}
// ==============================Password Toggle===========================================//


// =======================================Login functionality==================================//
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken'); 


const loginbtn = document.getElementById("loginbtn");
const error = document.getElementById("error")
const success = document.getElementById("success");

loginbtn && loginbtn.addEventListener("submit", (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  if (!username || !password) {
    error.textContent = "Username or Password Required";
    return;
  }

  const data = { username: username, password: password };

  fetch('/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken  
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        
        localStorage.setItem('role', data.role);  
        localStorage.setItem('permissions', JSON.stringify(data.permissions));  

        

        window.location.href = '/index';
      } else {
        error.textContent = data.message || "Invalid credentials";
      }
    })
    .catch(error => {
      console.error('Error', error);
      error.textContent = "An error occurred. Please try again.";
    });
});

// =======================================Login functionality==================================//

//========================================Setting information changing functionality==========================//
const changeusername = document.getElementById("changeusername")
const changeemail = document.getElementById("changemail")
const detailsChange = document.getElementById("detailsChange")

detailsChange && detailsChange.addEventListener("submit", (e) => {
  e.preventDefault();


  if (!changeusername.value || !changeemail.value) {
      error.textContent = "Username or Email must be filled";
  }

  const changingData = {
      newusername: changeusername.value,
      newemail: changeemail.value
  };

  fetch('settings', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken 
      },
      body: JSON.stringify(changingData) 
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          // window.location.href = '/settings';
          success.textContent = "Profile updated successfully"
      } else {
          error.textContent = data.message || "Invalid input";
      }
  })
  .catch(error => {
      console.error('Error:', error);
      error.textContent = "An error occurred. Please try again.";
  });
});
//========================================Setting information changing functionality==========================//

//========================================New Role Functionality==========================//
const roleForm = document.getElementById('roleForm')
roleForm && roleForm.addEventListener('submit', function(event) {
  event.preventDefault(); 

  // Get the role name and description
  const roleName = document.getElementById('roleName').value;
  const description = document.getElementById('description').value;
  const permissions = {
      venueManagement: {
          manageVenue: document.getElementById('manageVenue').checked,
          addVenue: document.getElementById('addVenue').checked,
          editVenue: document.getElementById('editVenue').checked,
          deleteVenue: document.getElementById('deleteVenue').checked
      },
      gameManagement: {
          manageGame: document.getElementById('manageGame').checked,
          addGame: document.getElementById('addGame').checked,
          editGame: document.getElementById('editGame').checked,
          removeGame: document.getElementById('removeGame').checked
      },
      ticketManagement: {
          viewTickets: document.getElementById('viewTickets').checked,
          updateTickets: document.getElementById('updateTickets').checked,
          addTickets: document.getElementById('addTickets').checked,
          deleteTickets: document.getElementById('deleteTickets').checked
      },
      userManagement: {
          manageUsers: document.getElementById('manageUsers').checked,
          addUsers: document.getElementById('addUsers').checked,
          editUsers: document.getElementById('editUsers').checked,
          deleteUsers: document.getElementById('deleteUsers').checked
      },
      roleManagement: {
          manageRoles: document.getElementById('manageRoles').checked,
          addRoles: document.getElementById('addRoles').checked,
          editRoles: document.getElementById('editRoles').checked,
          deleteRoles: document.getElementById('deleteRoles').checked
      },
      reportGeneration: {
          generateReports: document.getElementById('generateReports').checked,
          viewStats: document.getElementById('viewStats').checked,
          exportReports: document.getElementById('exportReports').checked
      },
      vendorManagement: {
          manageVendors: document.getElementById('manageVendors').checked,
          addVendors: document.getElementById('addVendors').checked,
          editVendors: document.getElementById('editVendors').checked,
          removeVendors: document.getElementById('removeVendors').checked
      },
      systemConfiguration: {
          configureSystem: document.getElementById('configureSystem').checked,
          customizeSystem: document.getElementById('customizeSystem').checked,
          manageIntegrations: document.getElementById('manageIntegrations').checked
      },
      customerSupport: {
          respondInquiries: document.getElementById('respondInquiries').checked
      }
  };

  if(!roleName || !description || !permissions){
    error.textContent = "All field are required"
  }

  const formData = {
      roleName,
      description,
      permissions
  }; 
  // Example of sending the data to a server
  
  fetch('users', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken 
    },
    body: JSON.stringify(formData)
}).then(response => response.json())
  .then(data => {
      console.log('Success:', data);
      error.textContent = data.error
      success.textContent = "Role created successfully"
    }).catch((err) => {
      console.error('Error:', err);
  });
});

//========================================New Role Functionality==========================//

//========================================New User Functionality==========================//
// app.js
const usercreateForm = document.getElementById("usercreateForm");

usercreateForm && usercreateForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const newusername = document.getElementById("username").value;
    const useremail = document.getElementById("useremail").value;
    const userpassword = document.getElementById("userpassword").value;
    const userrole = document.getElementById("userrole").value;

    const errorElement = document.getElementById("error");
    const successElement = document.getElementById("success");

    // Clear previous messages
    errorElement.textContent = "";
    successElement.textContent = "";

    if (!newusername || !useremail || !userpassword || !userrole) {
        errorElement.textContent = "All fields are required.";
        return;
    }

    const newUserData = {
        newusername: newusername,
        useremail: useremail,
        userpassword:userpassword,
        userrole: userrole
    };
 console.log(newUserData);
    fetch('users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken  // Ensure csrftoken is correctly defined
        },
        body: JSON.stringify(newUserData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            error.textContent = data.error;
        } else {
            success.textContent = data.message;
            usercreateForm.reset();
        }
    })
    .catch((err) => {
        console.error('Error:', err);
        error.textContent = 'An error occurred while creating the user.';
    });
});


//========================================New User Functionality==========================//

//========================================Logout functionality==========================//
const logout = document.getElementById("logout")
logout && logout.addEventListener("click", () => {
      fetch('logout', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrftoken
          },
      })
      .then(response => {
          if (response.ok) {
              return response.json();
          } else {
              throw new Error('Logout failed');
          }
      })
      .then(data => {
          window.location.href = "/";
      })
      .catch(error => {
          console.error('Error:', error);
          alert('An error occurred during logout. Please try again.');
      });
  })


//========================================Logout functionality==========================//



// ============================== Navbar Toggle ============================================//

function toggleSideNav() {
  const sideNav = document.querySelector(".sideNav");
  const button = document.querySelector(".open-btn");
  const buttonIcon = button.querySelector("i");

  if (sideNav.classList.contains("hidden")) {
    sideNav.classList.remove("hidden");
    button.classList.add("hidden"); // Hide the button
    buttonIcon.classList.remove("fa-angle-right");
    buttonIcon.classList.add("fa-angle-left");
  } else {
    sideNav.classList.add("hidden");
    button.classList.remove("hidden"); // Show the button
    buttonIcon.classList.remove("fa-angle-left");
    buttonIcon.classList.add("fa-angle-right");
  }
}

// ============================== Dashboard Permission check ============================================//



// ============================== Dashboard Permission check ============================================//

// ============================== Support ticket show ============================================//
// Call your API to fetch the tickets
fetch('http://localhost:8001/api/tickets/')  // Use the appropriate URL for your support ticket API
.then(response => response.json())
.then(data => {
    console.log(data);  // Verify the data structure in the browser's console

    // Select the UL element where we want to add the tickets
    const ticketList = document.getElementById('ticket-list');

    // Iterate through the ticket data
    data.forEach(ticket => {
        // Create an LI element for each ticket
        const ticketItem = document.createElement('li');
        ticketItem.classList.add('border-box', 'mt-3');  // Add classes

        // Create the inner HTML for each ticket
        ticketItem.innerHTML = `
            <div class="d-flex align-items-start justify-content-between">
                <div>
                    <div class="d-flex align-items-center">
                        <span class="ticketIcon"></span>
                        <h3 class="ticketHeading">Ticket# ${ticket.id}</h3>
                        <span class="ticketBadge">High Priority</span> 
                    </div>
                    <h4 class="ticketQuestion">${ticket.title}</h4>
                    <p class="ticketPara">${ticket.description
                      || 'No additional details provided.'}</p>  <!-- Assuming 'details' is in the API response -->
                </div>
                <span class="ticketPosting">Posted at ${new Date(ticket.created_at).toLocaleTimeString()}</span>  <!-- Formatting date -->
            </div>
            <div class="d-flex align-items-center justify-content-between borderBtm">
                <div class="d-flex align-items-center">
                    <img src="${ticket.profile_picture || '{% static "images/people.png" %}'}" alt=""
                         class="ticketImg">
                    <span class="ticketUserName">${ticket.user_name}</span>
                </div>
                <a href="/support-ticket-detail/${ticket.id}" class="ticketLink">Open Ticket</a>
            </div>
        `;

        // Append the ticket item to the list
        ticketList.appendChild(ticketItem);
    });
})
.catch(error => {
    console.error('Error fetching tickets:', error);
});

// ============================== Support ticket show ============================================//

// ============================== Navbar Toggle ============================================//
// ============================== ChartJS ============================================//
// ===============Dashboard Page ==================//
const balance = document.getElementById("balance");
new Chart(balance, {
  type: "line",
  data: {
    labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    datasets: [
      {
        label: "",
        data: [150, 175, 160, 200, 195, 225, 165, 170, 148, 135, 180, 162],
        backgroundColor: "#FEF0CD ",
        borderColor: "#F9C134 ",
        borderWidth: 3,
        fill: true,
        tension: 0.4,
      },
    ],
  },
  options: {
    animation: true,
    scales: {
      x: {
        display: true,
        grid: {
          display: false, // Disable grid lines on the y-axis
        },
      },
      y: {
        display: true,
        grid: {
          display: false, // Disable grid lines on the y-axis
        },
      },
    },
    plugins: {
      datalabels: {
        anchor: "end",
        align: "top",
        color: "black",
        font: {
          weight: "bold",
        },
        formatter: function (value, context) {
          return value; // Display the value on top of the bar
        },
      },
      legend: {
        display: false,
      },
    },
  },
});

const revenue = document.getElementById("revenue");
new Chart(revenue, {
  plugins: [ChartDataLabels],
  type: "pie",
  data: {
    labels: ["Battlefield", "Tekken", "FIFA 2024", "Call Of Ops", "Grid"],
    datasets: [
      {
        label: "",
        data: [10, 15, 30, 20, 25],
        backgroundColor: [
          "#00FF94",
          "#A0A0A0",
          "#FF6B00",
          "#9F69E8",
          "#FFBE4EF7",
        ],
        borderColor: ["#00FF94", "#A0A0A0", "#FF6B00", "#9F69E8", "#FFBE4EF7"],
        borderWidth: 2,
      },
    ],
  },
  options: {
    animation: true,
    aspectRatio: 1.2,
    plugins: {
      legend: {
        position: "top",
        labels: {
          boxWidth: 6,
          boxHeight: 6,
          color: "#000",
          font: {
            size: 14,
            weight: 400,
          },
        },
      },
      datalabels: {
        formatter: function (value, ctx) {
          var sum = 0;
          var dataArr = ctx.chart.data.datasets[0].data;
          dataArr.map(function (data) {
            sum += data;
          });
          var percentage = ((value * 100) / sum).toFixed(0) + "%";
          return percentage;
        },
        color: "#fff",
        font: {
          size: 12,
          weight: 600,
        },
        anchor: "end",
        align: "end",
        offset: -35,
      },
    },
  },
});

const ctx = document.getElementById("games").getContext("2d");

const gradient1 = ctx.createLinearGradient(0, 0, 0, 400);
gradient1.addColorStop(0, "rgba(0, 224, 150, 0.33)");
gradient1.addColorStop(1, "rgba(255, 255, 255, 0)");

const gradient2 = ctx.createLinearGradient(0, 0, 0, 400);
gradient2.addColorStop(0, "rgba(0, 157, 255, 0.32)");
gradient2.addColorStop(1, "rgba(0, 149, 255, 0)");

new Chart(ctx, {
  type: "line",
  data: {
    labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    datasets: [
      {
        label: "Multiplayer (4,504)",
        data: [150, 175, 160, 200, 195, 225, 165, 170, 148, 135, 180, 162],
        backgroundColor: gradient1,
        borderColor: "#07E098",
        borderWidth: 3,
        fill: true,
        tension: 0.4,
      },
      {
        label: "Arcade (3,004)",
        data: [165, 170, 148, 135, 180, 150, 175, 160, 200, 195, 225, 162],
        backgroundColor: gradient2,
        borderColor: "#0095FF",
        borderWidth: 3,
        fill: true,
        tension: 0.4,
      },
    ],
  },
  options: {
    animation: true,
    plugins: {
      legend: {
        position: "bottom",
        labels: {
          boxWidth: 12,
          boxHeight: 2,
          color: "#8B8B8B",
          font: {
            size: 16,
            weight: 400,
          },
        },
      },
    },
    scales: {
      x: {
        display: false,
        grid: {
          display: false,
        },
      },
      y: {
        display: false,
        grid: {
          display: false,
        },
      },
    },
  },
});
// ===============Dashboard Page ==================//

// ============================== ChartJS ============================================//
// =============== Hide Show Column Support Page ==================//
function hideShowDiv() {
  const columnElement = document.getElementById("ticketColumn");
  const hiddenElement = document.getElementById("ticketForm");
  const button = document.getElementById("ticketBtn");

  // Get the current state of the button
  const buttonState = button.getAttribute("data-state");

  if (buttonState === "new") {
    // When button is in 'new' state
    if (columnElement) {
      columnElement.classList.remove("col-lg-12");
      columnElement.classList.add("col-lg-8");
    }

    if (hiddenElement) {
      hiddenElement.classList.remove("d-none");
    }

    // Update button to 'cancel' state
    button.innerHTML = "Cancel";
    button.setAttribute("data-state", "cancel");
  } else {
    // When button is in 'cancel' state
    if (columnElement) {
      columnElement.classList.remove("col-lg-8");
      columnElement.classList.add("col-lg-12");
    }

    if (hiddenElement) {
      hiddenElement.classList.add("d-none");
    }

    // Update button to 'new' state
    button.innerHTML = '<i class="fas fa-plus me-2"></i> New Ticket';
    button.setAttribute("data-state", "new");
  }
}

// =============== Hide Show Column Support Page ==================//

// Select all submenu items
