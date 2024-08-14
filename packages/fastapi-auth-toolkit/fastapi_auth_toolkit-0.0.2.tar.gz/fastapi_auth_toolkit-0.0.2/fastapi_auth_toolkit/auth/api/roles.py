from fastapi import APIRouter

# from src.auth.schemas.roles import RoleCreateSchema, RoleUpdateSchema, RoleReadSchema
# from src.auth.services.auth import RoleService

roles_router = APIRouter()

#
# @roles_router.post("/", response_model=RoleReadSchema, status_code=status.HTTP_201_CREATED)
# async def create_role(role_create: RoleCreateSchema):
#     try:
#         created_role = await RoleService.create(role_create)
#         return created_role
#     except ValueError as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
#
#
# @roles_router.get("/{role_id}", response_model=RoleReadSchema)
# async def get_role(role_id: PydanticObjectId):
#     role = await RoleService.get(role_id)
#     if role is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
#     return role
#
#
# @roles_router.get("/", response_model=List[RoleReadSchema])
# async def get_all_roles():
#     roles = await RoleService.all()
#     return roles
#
#
# @roles_router.put("/{role_id}", response_model=RoleReadSchema)
# async def update_role(role_id: PydanticObjectId, role_update: RoleUpdateSchema):
#     try:
#         updated_role = await RoleService.update(role_id, role_update)
#         if updated_role is None:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
#         return updated_role
#     except ValueError as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
#
#
# @roles_router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_role(role_id: PydanticObjectId):
#     deleted = await RoleService.delete(role_id)
#     if not deleted:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
#     return {
#         ResponseKeyEnum.RESPONSE_CODE.value: "delete__success",
#         ResponseKeyEnum.MESSAGE.value: "Role deleted successfully",
#         ResponseKeyEnum.DETAIL.value: {
#             "id": role_id
#         }
#     }
