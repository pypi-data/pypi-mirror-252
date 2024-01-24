def get_elided_page_range(current_page, total_pages, display_count=5):
    if total_pages <= display_count:
        return list(range(1, total_pages + 1))

    # Determine the range of pages to display around the current page
    start_range = max(1, current_page - (display_count // 2))
    end_range = min(total_pages, start_range + display_count - 1)

    # Adjust the range if it reaches the start or end
    if end_range - start_range + 1 < display_count:
        start_range = max(1, end_range - display_count + 1)
    if end_range - start_range + 1 < display_count:
        end_range = min(total_pages, start_range + display_count - 1)

    # Add elision if necessary
    page_range = []
    if start_range > 1:
        page_range.append(1)
        if start_range > 2:
            page_range.append(None)

    page_range.extend(range(start_range, end_range + 1))

    if end_range < total_pages:
        if end_range < total_pages - 1:
            page_range.append(None)
        page_range.append(total_pages)

    return page_range