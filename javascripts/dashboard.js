document.addEventListener("DOMContentLoaded", () => {
    // Mock data
    const mockCommunities = [
      { id: 1, name: "Coding Club", members: 50, role: "Member" },
      { id: 2, name: "Art Circle", members: 30, role: "Admin" },
      { id: 3, name: "Environmental Warriors", members: 45, role: "Member" },
      { id: 4, name: "Business & Finance Society", members: 65, role: "Member" },
    ]
  
    const mockEvents = [
      { id: 1, title: "Fall Hackathon", type: "Academic", date: "2025-10-12", location: "Engineering Building" },
      { id: 2, title: "Art Exhibit", type: "Creative", date: "2025-11-01", location: "Student Center" },
      { id: 3, title: "Campus Clean-up", type: "Service", date: "2025-09-15", location: "Main Quad" },
      { id: 4, title: "Finance Workshop", type: "Academic", date: "2025-09-20", location: "Business School" },
      { id: 5, title: "Movie Night", type: "Social", date: "2025-09-25", location: "Outdoor Amphitheater" },
    ]
  
    const mockAnnouncements = [
      {
        id: 1,
        title: "New Campus Policy",
        content: "All students must complete the safety training by October 1st.",
        date: "2 hours ago",
      },
      {
        id: 2,
        title: "Library Hours Extended",
        content: "The library will now be open until midnight on weekdays.",
        date: "1 day ago",
      },
      {
        id: 3,
        title: "Career Fair Next Week",
        content: "Don't forget to prepare your resume for the upcoming career fair.",
        date: "2 days ago",
      },
    ]
  
    // Tab switching
    const tabButtons = document.querySelectorAll(".tab-button")
    const tabContents = document.querySelectorAll(".tab-content")
  
    tabButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const tabName = button.getAttribute("data-tab")
  
        // Deactivate all tabs
        tabButtons.forEach((btn) => btn.classList.remove("active"))
        tabContents.forEach((content) => content.classList.remove("active"))
  
        // Activate selected tab
        button.classList.add("active")
        document.getElementById(`${tabName}-tab`).classList.add("active")
      })
    })
  
    // Populate communities list
    const communitiesList = document.getElementById("communities-list")
    if (communitiesList) {
      mockCommunities.forEach((community) => {
        const communityItem = document.createElement("div")
        communityItem.className = "community-item"
        communityItem.innerHTML = `
          <div class="item-info">
            <div class="item-icon">
              <i data-lucide="users"></i>
            </div>
            <div class="item-details">
              <h4>${community.name}</h4>
              <p>${community.members} members</p>
            </div>
          </div>
          <div class="item-actions">
            <span class="badge ${community.role === "Admin" ? "badge-primary" : "badge-outline"}">${community.role}</span>
            <button class="btn btn-outline">View</button>
          </div>
        `
        communitiesList.appendChild(communityItem)
      })
  
      // Initialize Lucide icons for the newly added elements
      if (typeof lucide !== "undefined") {
        lucide.createIcons()
      }
    }
  
    // Event filtering
    const eventFilter = document.getElementById("event-filter")
    const eventsList = document.getElementById("events-list")
  
    function renderEvents(events) {
      if (!eventsList) return
  
      // Clear current events
      eventsList.innerHTML = ""
  
      if (events.length === 0) {
        // Show empty state
        const emptyState = document.createElement("div")
        emptyState.className = "empty-state"
        emptyState.innerHTML = `
          <i data-lucide="calendar"></i>
          <h3>No events found</h3>
          <p>There are no ${eventFilter.value !== "all" ? eventFilter.value : ""} events scheduled at this time.</p>
        `
        eventsList.appendChild(emptyState)
      } else {
        // Render events
        events.forEach((event) => {
          const eventItem = document.createElement("div")
          eventItem.className = "event-item"
          eventItem.innerHTML = `
            <div class="item-info">
              <div class="item-icon">
                <i data-lucide="calendar"></i>
              </div>
              <div class="item-details">
                <h4>${event.title}</h4>
                <p>${formatDate(event.date)} • ${event.location}</p>
              </div>
            </div>
            <div class="item-actions">
              <span class="badge badge-outline">${event.type}</span>
              <button class="btn btn-outline">Details</button>
            </div>
          `
          eventsList.appendChild(eventItem)
        })
      }
  
      // Initialize Lucide icons for the newly added elements
      if (typeof lucide !== "undefined") {
        lucide.createIcons()
      }
    }
  
    // Format date helper
    function formatDate(dateString) {
      const options = { year: "numeric", month: "long", day: "numeric" }
      return new Date(dateString).toLocaleDateString(undefined, options)
    }
  
    // Initial render of events
    if (eventsList) {
      renderEvents(mockEvents)
    }
  
    // Event filter change handler
    if (eventFilter) {
      eventFilter.addEventListener("change", function () {
        const filterValue = this.value
        const filteredEvents =
          filterValue === "all"
            ? mockEvents
            : mockEvents.filter((event) => event.type.toLowerCase() === filterValue.toLowerCase())
  
        renderEvents(filteredEvents)
      })
    }
  
    // Populate announcements list
    const announcementsList = document.getElementById("announcements-list")
    if (announcementsList) {
      mockAnnouncements.forEach((announcement) => {
        const announcementItem = document.createElement("div")
        announcementItem.className = "announcement-item"
        announcementItem.innerHTML = `
          <div class="announcement-header">
            <h4>${announcement.title}</h4>
            <span class="announcement-time">${announcement.date}</span>
          </div>
          <p class="announcement-content">${announcement.content}</p>
        `
        announcementsList.appendChild(announcementItem)
      })
    }
  
    // Logout button
    const logoutBtn = document.getElementById("logout-btn")
    if (logoutBtn) {
      logoutBtn.addEventListener("click", () => {
        // In a real app, you would clear auth state here
        window.location.href = "signin.html"
      })
    }
  })
  
  