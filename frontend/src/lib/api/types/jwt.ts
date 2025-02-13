import { z } from "zod";

export const JWTTokenSchema = z.object({
	accessToken: z.string(),
	refreshToken: z.string(),
	tokenType: z.string(),
});
export type JWTToken = z.infer<typeof JWTTokenSchema>;
