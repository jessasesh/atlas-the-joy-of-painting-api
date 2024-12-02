document.addEventListener("DOMContentLoaded", () => {
    const episodesTableBody = document.getElementById("episodes-table-body");
    const colorFilter = document.getElementById("color-filter");
    const subjectFilter = document.getElementById("subject-filter");
    const seasonFilter = document.getElementById("season-filter");
    const applyFiltersButton = document.getElementById("apply-filters");

    const populateTable = (data) => {
        episodesTableBody.innerHTML = "";

        if (data.length === 0) {
            const row = document.createElement("tr");
            const cell = document.createElement("td");
            cell.colSpan = 4;
            cell.textContent = "No episodes found.";
            cell.className = "text-center";
            row.appendChild(cell);
            episodesTableBody.appendChild(row);
            return;
        }

        data.forEach((episode) => {
            const row = document.createElement("tr");

            const titleCell = document.createElement("td");
            titleCell.textContent = episode.title || "N/A";
            row.appendChild(titleCell);

            const seasonCell = document.createElement("td");
            seasonCell.textContent = episode.season || "N/A";
            row.appendChild(seasonCell);

            const episodeNumberCell = document.createElement("td");
            episodeNumberCell.textContent = episode.episode_number || "N/A";
            row.appendChild(episodeNumberCell);

            const broadcastDateCell = document.createElement("td");
            broadcastDateCell.textContent = episode.broadcast_date || "N/A";
            row.appendChild(broadcastDateCell);

            episodesTableBody.appendChild(row);
        });
    };

    // Fetch data from API
    const fetchEpisodes = async () => {
        const color = colorFilter.value.trim();
        const subject = subjectFilter.value.trim();
        const season = seasonFilter.value.trim();

        let query = [];
        if (color) query.push(`color=${encodeURIComponent(color)}`);
        if (subject) query.push(`subject=${encodeURIComponent(subject)}`);
        if (season) query.push(`season=${encodeURIComponent(season)}`);
        const queryString = query.length ? `?${query.join("&")}` : "";

        try {
            const response = await fetch(`/api/episodes/filter${queryString}`);
            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }
            const data = await response.json();
            populateTable(data);
        } catch (error) {
            console.error("Error fetching data:", error);
            episodesTableBody.innerHTML = `
                <tr>
                    <td colspan="4" class="text-center text-danger">Failed to load episodes.</td>
                </tr>
            `;
        }
    };

    applyFiltersButton.addEventListener("click", fetchEpisodes);

    fetchEpisodes();
});
