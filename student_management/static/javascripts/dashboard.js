
document.addEventListener('DOMContentLoaded', () => {
    console.log('✅ JS loaded');

    function showToast(message) {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 3000);
    }

    function updateNotificationBadge() {
        const badge = document.querySelector('.notification-badge');
        let count = parseInt(badge.textContent) || 0;
        badge.textContent = count + 1;
    }

    const tabButtons = document.querySelectorAll(".tab-button");
    const tabContents = document.querySelectorAll(".tab-content");

    tabButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const tabName = button.getAttribute("data-tab");
            tabButtons.forEach((btn) => btn.classList.remove("active"));
            tabContents.forEach((content) => content.classList.remove("active"));
            document.getElementById(`${tabName}-tab`).classList.add("active");
            button.classList.add("active");
        });
    });

    const form = document.getElementById('create-community-form');
    const modal = document.getElementById('create-community-modal');
    const openBtn = document.getElementById('open-create-community');
    const closeBtn = document.getElementById('close-modal');
    const communitiesList = document.getElementById('communities-list');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const viewModal = document.getElementById('community-modal');
    const closeViewBtn = document.getElementById('close-community-modal');
    const modalName = document.getElementById('modal-community-name');
    const modalDescription = document.getElementById('modal-community-description');
    const deleteBtn = document.getElementById('delete-community-btn');

    let currentCommunityItem = null;
    let currentCommunityId = null;

    openBtn.addEventListener('click', () => { modal.style.display = 'flex'; });
    closeBtn.addEventListener('click', () => { modal.style.display = 'none'; });

    form.addEventListener('submit', async function(e) {
        e.preventDefault();  // Prevent default form submission
    
        const name = document.getElementById('community-name').value;
        const description = document.getElementById('community-description').value;
        const leaderId = document.getElementById('community-leader').value;
    
        const response = await fetch(createCommunityApiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                name,
                description,
                leader_id: parseInt(leaderId)
            })
        });
    
        if (response.ok) {
            const data = await response.json();
            console.log(data);  // Debugging: Check API response
            // Close modal and reset form
            form.reset();
            modal.style.display = 'none';
    
            // Update the community list...
        } else {
            alert('Error creating community');
        }
    });
    

    function attachViewButton(button, communityItem) {
        button.addEventListener('click', async () => {
            const id = communityItem.dataset.id;
            try {
                const response = await fetch(`/student/communities/${id}/details/`);
                if (response.ok) {
                    const data = await response.json();
                    modalName.textContent = data.name;
                    modalDescription.textContent = data.description;
                    currentCommunityItem = communityItem;
                    currentCommunityId = id;
                    viewModal.style.display = 'flex';
                } else {
                    alert('Failed to load community details.');
                }
            } catch (error) {
                console.error('Error fetching details:', error);
                alert('An error occurred.');
            }
        });
    }

    document.querySelectorAll('.view-btn').forEach(button => {
        const communityItem = button.closest('.community-item');
        attachViewButton(button, communityItem);
    });

    deleteBtn.addEventListener('click', async () => {
        if (!currentCommunityId) {
            alert('No community selected.');
            return;
        }
        if (confirm('Are you sure you want to delete this community?')) {
            const response = await fetch(`/student/communities/${currentCommunityId}/delete/`, {
                method: 'DELETE',
                headers: { 'X-CSRFToken': csrfToken }
            });

            if (response.ok) {
                currentCommunityItem.remove();
                viewModal.style.display = 'none';
                updateNotificationBadge();
                showToast('❌ Community deleted!');
            } else {
                alert('Failed to delete community.');
            }
        }
    });

    closeViewBtn.addEventListener('click', () => viewModal.style.display = 'none');
    window.addEventListener('click', (event) => {
        if (event.target === viewModal) viewModal.style.display = 'none';
    });

    const searchInput = document.getElementById('community-search-input');
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            const query = searchInput.value.toLowerCase();
            document.querySelectorAll('.community-item').forEach(item => {
                const name = item.querySelector('h4').textContent.toLowerCase();
                const description = item.querySelector('p').textContent.toLowerCase();
                item.style.display = (name.includes(query) || description.includes(query)) ? '' : 'none';
            });
        });
    }
});



