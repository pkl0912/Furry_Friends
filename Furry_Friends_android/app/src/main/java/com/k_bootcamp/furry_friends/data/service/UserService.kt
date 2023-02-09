package com.k_bootcamp.furry_friends.data.service

import com.k_bootcamp.furry_friends.data.response.user.Session
import com.k_bootcamp.furry_friends.data.response.user.SessionResponse
import com.k_bootcamp.furry_friends.data.response.user.SignInResponse
import com.k_bootcamp.furry_friends.model.user.LoginUser
import com.k_bootcamp.furry_friends.model.user.SignInUser
import retrofit2.Response
import retrofit2.http.*

interface UserService {
    // 로그인
    @POST("/login")
    suspend fun loginUser(
        @Body user: LoginUser
    ): Response<SessionResponse>

    // 정보가져오기
    @GET("/{sessionId}")  //// session 객체로 교환 필요
    suspend fun getInfo(
        @Path("sessionId") sessionId: String?
    ): Response<String>

    // 회원가입
    @POST("/register")
    suspend fun signInUser(
        @Body user: SignInUser
    ): Response<SignInResponse>

    @GET("/logout")
    suspend fun logoutUser(): Response<Void>
}