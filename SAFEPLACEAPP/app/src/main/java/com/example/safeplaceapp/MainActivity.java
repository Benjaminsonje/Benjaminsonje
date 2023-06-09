package com.example.safeplaceapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.material.button.MaterialButton;

public class MainActivity extends AppCompatActivity {


    private Button button;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button button = (Button) findViewById(R.id.nextbtn);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openMainActivity2();

            }
        });
    }
    public void openMainActivity2(){
        EditText editText = (EditText) findViewById(R.id.email);
        String text = editText.getText().toString();

        EditText editText1 = (EditText) findViewById(R.id.pass);
        int number = Integer .parseInt(editText1.getText().toString());
        Intent intent = new Intent(this, MainActivity2.class);
        startActivity(intent);
    }
}
