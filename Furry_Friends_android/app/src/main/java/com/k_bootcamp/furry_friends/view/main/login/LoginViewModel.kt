package com.k_bootcamp.furry_friends.view.main.login

import android.content.Context
import androidx.lifecycle.LiveData
import androidx.lifecycle.MediatorLiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import com.fc.baeminclone.screen.base.BaseViewModel
import com.k_bootcamp.furry_friends.R
import com.k_bootcamp.furry_friends.data.repository.user.UserRepository
import com.k_bootcamp.furry_friends.data.response.user.Session
import com.k_bootcamp.furry_friends.model.user.LoginUser
import dagger.hilt.android.lifecycle.HiltViewModel
import dagger.hilt.android.qualifiers.ActivityContext
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class LoginViewModel @Inject constructor(
    private val userRepository: UserRepository,
    @ApplicationContext private val context: Context
) : BaseViewModel() {
    private val _isLogin = MutableLiveData<LoginState>()
    val isLogin: LiveData<LoginState>
        get() = _isLogin

    val getInfo: MutableLiveData<String> = MutableLiveData<String>()
    val emailLiveData: MutableLiveData<String> = MutableLiveData()
    val pwdLiveData: MutableLiveData<String> = MutableLiveData()


    val isValidLiveData: MediatorLiveData<Boolean> = MediatorLiveData<Boolean>().apply {
        // 입력이 valid 하지않으면 버튼 disabled
        this.value = false

        addSource(emailLiveData) {
            this.value = validateForm()
        }

        addSource(pwdLiveData) {
            this.value = validateForm()
        }
    }

    private fun validateForm(): Boolean {
        return !emailLiveData.value.isNullOrBlank() && !pwdLiveData.value.isNullOrBlank()
    }

    fun getSessionRequest(user: LoginUser) {
        _isLogin.value = LoginState.Loading
        viewModelScope.launch(Dispatchers.IO) {
            val session = userRepository.loginUser(user)
            session?.let {
                _isLogin.postValue(
                    LoginState.Success(
                        it.sesionId
                    )
                )
            } ?: kotlin.run {
                _isLogin.postValue(LoginState.Error(context.getString(R.string.failed_login)))
            }
        }

    }
    fun getUserInfo(sessionId: String) = viewModelScope.launch(Dispatchers.IO) {
        val response = userRepository.getInfo(sessionId)
        response?.let {
            getInfo.postValue(response ?: context.getString(R.string.error_response))
        } ?: kotlin.run {
            getInfo.postValue(context.getString(R.string.error_response))
        }
    }
}

