from interface.web.routes.comment.contracts.output.get_categories import CommentOutputContract


GET_PRODUCT_COMMENTS = {
    200: {
        "description": "Product's comments are returned.",
        "model": list[CommentOutputContract],
    },
}
