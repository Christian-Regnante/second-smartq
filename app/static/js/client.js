let selectedOrg = null;
let selectedService = null;
let services = [];

// Load organizations on page load
document.addEventListener('DOMContentLoaded', loadOrganizations);

async function loadOrganizations() {
    try {
        const response = await fetch('/client/api/organizations');
        const orgs = await response.json();
        
        const select = document.getElementById('organizationSelect');
        orgs.forEach(org => {
            const option = document.createElement('option');
            option.value = org.id;
            option.textContent = org.name;
            select.appendChild(option);
        });
        
        select.addEventListener('change', (e) => {
            if (e.target.value) {
                selectedOrg = parseInt(e.target.value);
                loadServices();
            }
        });
    } catch (error) {
        console.error('Error loading organizations:', error);
    }
}

async function loadServices() {
    try {
        const response = await fetch(`/client/api/services?org_id=${selectedOrg}`);
        services = await response.json();
        
        const container = document.getElementById('serviceButtons');
        container.innerHTML = services.map(service => 
            `<div class="service-btn" onclick="selectService(${service.id})">${service.name}</div>`
        ).join('');
        
        document.getElementById('service-selection').style.display = 'block';
    } catch (error) {
        console.error('Error loading services:', error);
    }
}

function selectService(serviceId) {
    selectedService = serviceId;
    document.getElementById('service-selection').style.display = 'none';
    document.getElementById('phone-input').style.display = 'block';
}

function goBack() {
    selectedService = null;
    document.getElementById('phone-input').style.display = 'none';
    document.getElementById('service-selection').style.display = 'block';
}


function goBackorg() {
    selectedOrg = null;
    selectedService = null;
    document.getElementById('organizationSelect').value = '';
    document.getElementById('service-selection').style.display = 'none';
    document.getElementById('org-selection').style.display = 'block';
}

async function joinQueue() {
    const phone = document.getElementById('phoneNumber').value;
    
    if (!phone || phone.length < 10) {
        alert('Please enter a valid phone number');
        return;
    }
    
    try {
        const response = await fetch('/client/api/join-queue', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                service_id: selectedService,
                phone_number: phone
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('queueNumber').textContent = data.queue_number;
            document.getElementById('counter').textContent = data.counter;
            document.getElementById('position').textContent = data.position;
            document.getElementById('waitTime').textContent = data.estimated_wait;
            
            document.getElementById('phone-input').style.display = 'none';
            document.getElementById('ticket-display').style.display = 'block';
        } else {
            alert(data.error || 'Failed to join queue');
        }
    } catch (error) {
        console.error('Error joining queue:', error);
        alert('Failed to join queue');
    }
}

function reset() {
    selectedOrg = null;
    selectedService = null;
    document.getElementById('organizationSelect').value = '';
    document.getElementById('phoneNumber').value = '';
    document.getElementById('ticket-display').style.display = 'none';
    document.getElementById('org-selection').style.display = 'block';
    document.getElementById('service-selection').style.display = 'none';
}