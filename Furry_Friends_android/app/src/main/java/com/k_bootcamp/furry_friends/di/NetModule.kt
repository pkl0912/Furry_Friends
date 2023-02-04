package com.k_bootcamp.furry_friends.di

import com.k_bootcamp.furry_friends.data.service.UserService
import com.k_bootcamp.furry_friends.data.url.Url
import com.k_bootcamp.furry_friends.util.etc.IoDispatcher
import com.k_bootcamp.furry_friends.util.etc.MainDispatcher
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.Dispatchers
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.converter.scalars.ScalarsConverterFactory
import javax.inject.Singleton

@InstallIn(SingletonComponent::class)
@Module
class NetModule {

    @Singleton
    @Provides
    fun providesUserService(okHttpClient: OkHttpClient): UserService {
        return Retrofit.Builder()
            .addConverterFactory(ScalarsConverterFactory.create())
            .addConverterFactory(GsonConverterFactory.create())
            .baseUrl(Url.BASE_URL)
            .client(okHttpClient)
            .build().create(UserService::class.java)
    }
}