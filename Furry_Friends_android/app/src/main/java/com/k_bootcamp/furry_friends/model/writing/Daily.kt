package com.k_bootcamp.furry_friends.model.writing

import com.google.gson.annotations.SerializedName

// 임시 모델
data class Daily(
    @SerializedName("title")
    val title: String,
    @SerializedName("image")
    val imageUrl: String,
    @SerializedName("content")
    val content: String,
    @SerializedName("currdate")
    val currdate:String
)
