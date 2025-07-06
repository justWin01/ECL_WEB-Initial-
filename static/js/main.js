// Toast notification logic
document.addEventListener("DOMContentLoaded", () => {
    const toast = document.getElementById('toast');
    const params = new URLSearchParams(window.location.search);
    if (params.get('favorited')) {
      toast.classList.remove('hidden');
      setTimeout(() => toast.classList.add('hidden'), 3000);
    }
  
    // Toggle profile menu
    const profileBtn = document.getElementById('profileBtn');
    const profileMenu = document.getElementById('profileMenu');
  
    if (profileBtn && profileMenu) {
      profileBtn.addEventListener('click', (e) => {
        e.stopPropagation(); // prevent window click
        profileMenu.classList.toggle('hidden');
      });
  
      // Close menu if clicking outside
      window.addEventListener('click', (e) => {
        if (!profileMenu.contains(e.target) && !profileBtn.contains(e.target)) {
          profileMenu.classList.add('hidden');
        }
      });
    }
  });
  