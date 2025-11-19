import { BaseApiRoute } from "$lib/api/routes/BaseApiRoute";
import type { UserUpdate, UserCreate } from "$lib/api/types/user";

export class UsersApiRoute extends BaseApiRoute<UserCreate, UserUpdate> {
	constructor() {
		super("/api/users/");
	}
}
