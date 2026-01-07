def normalize_query_params(params: dict) -> dict[str, str]:
    return {
        k: ("true" if v else "false") if isinstance(v, bool) else str(v)
        for k, v in params.items()
        if v is not None
    }
