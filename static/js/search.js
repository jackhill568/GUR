document.addEventListener("DOMContentLoaded", function() {
    const resultsContainer = document.getElementById("results");
    const queryInput = document.getElementById("search-query");
    let nextPage = parseInt(document.getElementById("next-page").value);
    const query = queryInput ? queryInput.value : "";

    if (!resultsContainer || !query) return;

    let isLoading = false;

    window.addEventListener("scroll", () => {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
            if (!nextPage || isLoading) return;

            isLoading = true;

						const params = new URLSearchParams({ q: query, page: nextPage });

						fetch(`${window.location.pathname}?${params.toString()}`, {
						    headers: { "X-Requested-With": "XMLHttpRequest" }
						})
						.then(res => res.json())
						.then(data => {
						    resultsContainer.insertAdjacentHTML("beforeend", data.html);
						    nextPage = data.next_page;
						    isLoading = false;
						})
						.catch(err => {
						    console.error("Error loading more results:", err);
						    isLoading = false;
						});
        }
    });
});
